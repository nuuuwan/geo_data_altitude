from functools import cache

import numpy as np
from utils import Log

from alt_lk.data.JSONCombinedAltFile import JSONCombinedAltFile

log = Log('matrices')

DIM = 1201
DIM2 = DIM * 5

PLACE_TO_LATLNG = dict(
    Pidurutalagala=(7.001088543413415, 80.77359079838624),
    Kirigalpotta=(6.798901150827766, 80.76869492704733),
    Totupola=(6.840831049419954, 80.82203861344966),
    SriPada=(6.809375874868926, 80.49935558978555),
    Namunukula=(6.933503385286176, 81.1166237829777),
    Gongala=(6.382356658191272, 80.64370457201038),
    Sirigiya=(7.95706456054186, 80.7602891865722),
    Maligakanda=(6.927929860706534, 79.87078444765905),
    TownHall=(6.915689639180558, 79.86361271106342),
    Jaffna=(9.661201406066375, 80.024472380371),
    Kandy=(7.293117260836311, 80.63503899171117),
    Matara=(5.94316208005024, 80.54953656638747),
    Batticaloa=(7.717991517426244, 81.69893023425655),
)


def _(latlng: tuple[float]) -> tuple[int]:
    lat, lng = latlng
    i_lat = 6005 - int((lat - 5) * DIM)
    i_lng = int((lng - 78) * DIM)
    return (i_lat, i_lng)


@cache
def get_alt_matrix():
    return np.array(JSONCombinedAltFile().read())


@cache
def get_latlng_matrix():
    m_alt = get_alt_matrix()
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
    # Convert latitudes and longitudes to radians
    lat0, lng0 = latlng0
    lat0, lng0 = np.radians(lat0), np.radians(lng0)

    latlng_matrix_rad = np.radians(latlng_matrix)

    # Calculate differences in latitude and longitude
    dlat = latlng_matrix_rad[:, :, 0] - lat0
    dlng = latlng_matrix_rad[:, :, 1] - lng0

    # Haversine formula
    a = (
        np.sin(dlat / 2) ** 2
        + np.cos(lat0)
        * np.cos(latlng_matrix_rad[:, :, 0])
        * np.sin(dlng / 2) ** 2
    )
    c = 2 * np.arcsin(np.sqrt(a))

    # Radius of the Earth in kilometers
    earth_radius = 6371

    # Calculate the distance
    distance = earth_radius * c

    return distance


def get_distance_matrix(latlng0):
    m_latlng = get_latlng_matrix()
    return haversine_vectorized(latlng0, m_latlng)


if __name__ == '__main__':
    m_alt = get_alt_matrix()
    log.debug('Loaded m_alt')
    m_latlng = get_latlng_matrix()
    m_distance = get_distance_matrix(PLACE_TO_LATLNG['TownHall'])
    for place, latlng in PLACE_TO_LATLNG.items():
        idx = _(latlng)
        print(place, m_alt[idx], m_latlng[idx], m_distance[idx])
