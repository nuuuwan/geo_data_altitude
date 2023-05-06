from utils import Log

from alt_lk.compute._constants import (DIM_X, DIM_Y, MAX_ALPHA, MAX_BETA,
                                       MAX_DISTANCE, MIN_ALPHA, MIN_BETA)
from alt_lk.compute.matrices import _
from alt_lk.data.Places import Places

log = Log('labels')


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

        min_distance = pers.get(x, {}).get(y, MAX_DISTANCE)

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
        beta = 0.09

        x = int(DIM_X * (alpha - MIN_ALPHA) / (MAX_ALPHA - MIN_ALPHA))
        y = int(DIM_Y * (MAX_BETA - beta) / (MAX_BETA - MIN_BETA))

        icon = '●'
        label_info_list.append(dict(xy=(x, y), name=icon + d['name']))
    return label_info_list


def dedupe(info_list):
    idx = {}
    for info in sorted(info_list, key=lambda d: d.get('alt', 0)):
        x = info['xy'][0]
        x2 = x // 10
        idx[x2] = info
    return list(idx.values())


def get_label_info_list(m_alpha, m_beta, m_distance, pers):
    return dedupe(
        get_mountain_labels(m_alpha, m_beta, m_distance, pers)
        + get_building_labels(m_alpha)
    )
