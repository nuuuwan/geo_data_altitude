import colorsys
import math
import time
import webbrowser

import numpy as np
from utils import Log

from alt_lk.compute.matrices import (_, get_alpha_matrix, get_alt_matrix,
                                     get_beta_matrix, get_distance_matrix,
                                     get_latlng_matrix)
from alt_lk.data.Places import Places
from alt_lk.render.AbstractMap import AbstractMap

log = Log('matrices')

DIM = 1201
DIM2 = DIM * 5
MAX_DISTANCE = 100

MIN_ALPHA, MAX_ALPHA = 90 - 45, 90 + 45
MIN_BETA, MAX_BETA = 0, 2
DIM_Y = 500
DIM_X = int(DIM_Y * (MAX_ALPHA - MIN_ALPHA) / (MAX_BETA - MIN_BETA) / 2)


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


def get_peak_list(idx, pers, m_latlng, m_alt, m_beta):
    peak_list = []
    for i_x in range(DIM_X):
        dis0 = pers[DIM_Y - 1, i_x]
        peak = None
        for i_y in range(DIM_Y):
            dis = pers[i_y, i_x]
            if dis != dis0 and (i_x, i_y) in idx:
                i_lat, i_lng = idx[(i_x, i_y)]
                lat, lng = m_latlng[i_lat, i_lng]
                alt = m_alt[i_lat, i_lng]
                beta = m_beta[i_lat, i_lng]
                peak = dict(
                    alt=alt,
                    beta=beta,
                    latlng=(lat, lng),
                )
                break
        peak_list.append(peak)
    return peak_list


def analyze_peaks(idx, pers, m_latlng, m_alt, m_beta):
    peak_list = get_peak_list(idx, pers, m_latlng, m_alt, m_beta)
    WINDOW = 100
    i_display_peaks = 0
    for i_x in range(WINDOW, DIM_X - WINDOW):
        peak = peak_list[i_x]
        if not peak:
            continue
        local_peak_list = peak_list[i_x - WINDOW: i_x + WINDOW]
        max_beta = max(
            peak['beta'] if peak else 0 for peak in local_peak_list
        )
        if peak['beta'] != max_beta:
            continue

        min_d = 100

        for d in Places.mountains():
            latlng_mountain = d['latlng']
            dlat, dlng = (
                peak['latlng'][0] - latlng_mountain[0],
                peak['latlng'][1] - latlng_mountain[1],
            )
            d = math.sqrt(dlat * dlat + dlng * dlng)
            if d < min_d:
                min_d = d

        if min_d < 0.002:
            continue

        alt = peak['alt']
        print(
            str(peak['latlng'][0]) + ',' + str(peak['latlng'][1]),
            '\t',
            alt * 1_000,
        )
        url = 'https://www.google.lk/maps/place/' + str(peak['latlng'])
        webbrowser.open(url)
        time.sleep(0.5)
        i_display_peaks += 1
        if i_display_peaks >= 10:
            break


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


if __name__ == '__main__':
    LATLNG0 = (6.9188473380988125, 79.85911404345833)
    m_alpha = get_alpha_matrix(LATLNG0)
    m_beta = get_beta_matrix(LATLNG0)
    m_distance = get_distance_matrix(LATLNG0)
    m_latlng = get_latlng_matrix()
    m_alt = get_alt_matrix()

    pers = get_perspective(m_alpha, m_beta, m_distance, m_latlng, m_alt)
    label_info_list = get_label_info_list(m_alpha, m_beta, m_distance, pers)
    AbstractMap(pers, get_color_perspective, label_info_list).write()
