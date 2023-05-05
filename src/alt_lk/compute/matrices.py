import math

import numpy as np
from utils import Log

from alt_lk.data.JSONCombinedAltFile import JSONCombinedAltFile

log = Log('matrices')

DIM = 1201
DIM2 = DIM * 5
MAX_DISTANCE = 100


h0 = 0.15
R = 6371
d = math.sqrt(2 * R * h0)
print(f'{R=}km, {h0=}km, {d=}km')


def _(latlng: tuple[float]) -> tuple[int]:
    lat, lng = latlng
    i_lat = 6005 - int((lat - 5) * DIM)
    i_lng = int((lng - 78) * DIM)
    return (i_lat, i_lng)


def get_alt_matrix():
    return np.array(JSONCombinedAltFile().read()) / 1_000


def get_latlng_matrix(m_alt):
    return np.array(
        [
            [
                (5 + (DIM2 - i) / DIM, 78 + j / DIM)
                for j, alt in enumerate(row)
                if alt != -32768
            ]
            for i, row in enumerate(m_alt)
        ]
    )


def haversine_vectorized(latlng0, latlng_matrix):
    lat0, lng0 = latlng0
    lat0, lng0 = np.radians(lat0), np.radians(lng0)

    latlng_matrix_rad = np.radians(latlng_matrix)

    dlat = latlng_matrix_rad[:, :, 0] - lat0
    dlng = latlng_matrix_rad[:, :, 1] - lng0

    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat0)
        * np.cos(latlng_matrix_rad[:, :, 0])
        * np.sin(dlng / 2) ** 2
    )
    c = 2 * np.arcsin(np.sqrt(a))

    distance = R * c

    return distance


def get_distance_matrix(latlng0, m_latlng):
    return haversine_vectorized(latlng0, m_latlng)


def get_alpha_matrix(latlng0, m_latlng):
    lat0, lng0 = latlng0
    lat0, lng0 = np.radians(lat0), np.radians(lng0)

    latlng_matrix_rad = np.radians(m_latlng)

    dlat = latlng_matrix_rad[:, :, 0] - lat0
    dlng = latlng_matrix_rad[:, :, 1] - lng0
    atan = np.arctan2(dlat, dlng)
    return 90 - np.degrees(atan)


def get_beta_matrix(m_alt, m_distance):
    D = m_distance - d
    b = D**2 / (2 * R)

    x = D * (m_alt - b) / (R + b)
    y = x * (R / D)
    rad = np.arctan2(x + m_distance, y)
    return 90 - np.degrees(rad)
