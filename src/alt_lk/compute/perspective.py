import colorsys

import numpy as np
from scipy.ndimage import minimum_filter
from utils import Log

from alt_lk.compute._constants import (DIM_X, DIM_Y, MAX_ALPHA, MAX_BETA,
                                       MAX_DISTANCE, MIN_ALPHA, MIN_BETA)
from alt_lk.compute.matrices import (_, get_alpha_matrix, get_alt_matrix,
                                     get_beta_matrix, get_distance_matrix,
                                     get_latlng_matrix)
from alt_lk.data.Places import Places
from alt_lk.render.AbstractMap import AbstractMap

log = Log('matrices')


def get_mountain_labels(m_alpha, m_beta, m_distance, pers):
    label_info_list = []
    for d in Places.mountains():
        latlng = d['latlng']
        i_lat, i_lng = _(latlng)
        alpha, beta, distance = (
            m_alpha[i_lat, i_lng],
            m_beta[i_lat, i_lng],
            m_distance[i_lat, i_lng],
        )

        if not (MIN_ALPHA < alpha <= MAX_ALPHA):
            continue
        if not (MIN_BETA < beta <= MAX_BETA):
            continue

        x = int(DIM_X * (alpha - MIN_ALPHA) / (MAX_ALPHA - MIN_ALPHA))
        y = int(DIM_Y * (MAX_BETA - beta) / (MAX_BETA - MIN_BETA))

        min_distance = pers[y, x]
        icon = '▲'
        if distance < min_distance + 10:
            label_info_list.append(
                dict(xy=(x, y), name=icon + d['name'], alt=d['alt'])
            )
    return label_info_list


def get_building_labels(m_alpha):
    label_info_list = []
    for d in Places.buildings():
        latlng = d['latlng']
        i_lat, i_lng = _(latlng)
        alpha = m_alpha[i_lat, i_lng]

        if not (MIN_ALPHA < alpha <= MAX_ALPHA):
            continue
        beta = 0.07

        x = int(DIM_X * (alpha - MIN_ALPHA) / (MAX_ALPHA - MIN_ALPHA))
        y = int(DIM_Y * (MAX_BETA - beta) / (MAX_BETA - MIN_BETA))

        icon = '□'
        label_info_list.append(dict(xy=(x, y), name=icon + d['name']))
    return label_info_list


def get_perspective(m_alpha, m_beta, m_distance, m_latlng, m_alt):
    n_lat, n_lng = m_alpha.shape
    idx = {}
    pers = np.ones((DIM_Y, DIM_X)) * MAX_DISTANCE
    for i_lat in range(n_lat):
        for i_lng in range(n_lng):
            beta0 = m_beta[i_lat, i_lng]
            if not (MIN_BETA < beta0 <= MAX_BETA):
                continue
            alpha = m_alpha[i_lat, i_lng]
            if not (MIN_ALPHA < alpha <= MAX_ALPHA):
                continue

            i_x0 = int(DIM_X * (alpha - MIN_ALPHA) / (MAX_ALPHA - MIN_ALPHA))
            i_y0 = int(DIM_Y * (MAX_BETA - beta0) / (MAX_BETA - MIN_BETA))
            new_val = m_distance[i_lat, i_lng]

            for i_y in range(i_y0, DIM_Y):
                cur_val = pers[i_y, i_x0]
                if not (cur_val == 0 or new_val < cur_val):
                    continue
                pers[i_y, i_x0] = new_val
                if i_y0 != i_y:
                    continue
                idx[(i_x0, i_y0)] = (i_lat, i_lng)

    return pers


def get_label_info_list(m_alpha, m_beta, m_distance, pers):
    return get_mountain_labels(
        m_alpha, m_beta, m_distance, pers
    ) + get_building_labels(m_alpha)


def get_color_perspective(distance):
    if distance == MAX_DISTANCE:
        return (0, 128, 255)
    p_distance = min(MAX_DISTANCE, distance) / MAX_DISTANCE

    hue = 150 * (1 - p_distance)
    saturation = 100
    light = 10 + 40 * p_distance

    # hue = 0
    # saturation = 0
    # light = 30 + 40 * p_distance

    (r, g, b) = colorsys.hls_to_rgb(hue / 360, light / 100, saturation / 100)
    return tuple(int(255 * x) for x in (r, g, b))


def perspective_pipeline(latlng0):
    m_alt = get_alt_matrix()
    log.debug('m_alt computed.')
    m_latlng = get_latlng_matrix(m_alt)
    log.debug('m_latlng computed.')

    m_alpha = get_alpha_matrix(latlng0, m_latlng)
    log.debug('m_alpha computed.')

    m_distance = get_distance_matrix(latlng0, m_latlng)
    log.debug('m_distance computed.')

    m_beta = get_beta_matrix(m_alt, m_distance)
    log.debug('m_beta computed.')

    pers = get_perspective(m_alpha, m_beta, m_distance, m_latlng, m_alt)
    pers = minimum_filter(pers, size=5)
    log.info('pers computed.')

    label_info_list = get_label_info_list(m_alpha, m_beta, m_distance, pers)

    AbstractMap(pers, get_color_perspective, label_info_list).write()


if __name__ == '__main__':
    LATLNG0 = (6.9188473380988125, 79.85911404345833)
    perspective_pipeline(LATLNG0)
