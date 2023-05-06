import colorsys

from utils import FiledVariable, Log

from alt_lk.compute._constants import (DIM_X, DIM_Y, LATLNG0, MAX_ALPHA,
                                       MAX_BETA, MAX_DISTANCE, MIN_ALPHA,
                                       MIN_BETA)
from alt_lk.compute.labels import get_label_info_list
from alt_lk.compute.matrices import (get_alpha_matrix, get_alt_matrix,
                                     get_beta_matrix, get_distance_matrix,
                                     get_latlng_matrix)
from alt_lk.render.LineMap import LineMap

log = Log('matrices')


def get_line_info_idx(m_alpha, m_beta, m_distance):
    n_lat, n_lng = m_alpha.shape
    idx = {}
    for i_lat in range(n_lat):
        for i_lng in range(n_lng):
            alpha = m_alpha[i_lat, i_lng]
            beta = m_beta[i_lat, i_lng]
            if not all(
                [
                    MIN_ALPHA < alpha <= MAX_ALPHA,
                    MIN_BETA < beta <= MAX_BETA,
                ]
            ):
                continue

            x = int(DIM_X * (alpha - MIN_ALPHA) / (MAX_ALPHA - MIN_ALPHA))
            y = int(DIM_Y * (MAX_BETA - beta) / (MAX_BETA - MIN_BETA))
            distance = m_distance[i_lat, i_lng]

            if x not in idx:
                idx[x] = []
            idx[x].append(dict(x=x, y=y, distance=distance))
    return idx


def get_line_info_list_nocache(idx):
    line_info_list = []
    line_info_pers_idx = {}
    for x, info_list in idx.items():
        sorted_info_list = sorted(info_list, key=lambda d: d['distance'])
        y2 = DIM_Y
        line_info_pers_idx[x] = {}
        for info in sorted_info_list:
            y1 = info['y']
            if y1 < y2:
                distance = info['distance']
                line_info = dict(
                    x=info['x'],
                    y1=y1,
                    y2=y2,
                    distance=distance,
                )
                line_info_list.append(line_info)
                for y in range(y1, y2):
                    line_info_pers_idx[x][y] = distance
                y2 = y1

    return [line_info_list, line_info_pers_idx]


def get_line_info_list(latlng0, m_alpha, m_beta, m_distance):
    def func_get():
        idx = get_line_info_idx(m_alpha, m_beta, m_distance)
        return get_line_info_list_nocache(idx)

    lat0, lng0 = latlng0
    return FiledVariable(
        f'line-info-list-{lat0:.4f}-{lng0:.4f}-v3', func_get
    ).value


def get_color_perspective(distance):
    if distance == MAX_DISTANCE:
        return (0, 128, 255)
    MAX_DISTANCE2 = 80
    p_distance = min(MAX_DISTANCE2, distance) / MAX_DISTANCE2

    hue = 150 * (1 - p_distance)
    saturation = 100
    light = 10 + 30 * p_distance

    # hue = 0
    # saturation = 0
    # light = 30 + 40 * p_distance

    (r, g, b) = colorsys.hls_to_rgb(hue / 360, light / 100, saturation / 100)
    # return tuple(int(255 * x) for x in (r, g, b))
    hex_color = f'#{int(r * 255):02X}{int(g * 255):02X}{int(b * 255):02X}'
    return hex_color


def perspective_pipeline(latlng0):
    m_alt = get_alt_matrix()
    m_latlng = get_latlng_matrix(m_alt)
    m_alpha = get_alpha_matrix(latlng0, m_latlng)
    m_distance = get_distance_matrix(latlng0, m_latlng)
    m_beta = get_beta_matrix(latlng0, m_alt, m_distance)

    [line_info_list, line_info_pers_idx] = get_line_info_list(
        latlng0, m_alpha, m_beta, m_distance
    )
    label_info_list = get_label_info_list(
        m_alpha, m_beta, m_distance, line_info_pers_idx
    )
    LineMap(line_info_list, get_color_perspective, label_info_list).write()


if __name__ == '__main__':
    perspective_pipeline(LATLNG0)
