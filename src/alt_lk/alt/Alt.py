import os
from dataclasses import dataclass
from functools import cache

from utils import Log

from alt_lk.core.BBox import BBox
from alt_lk.core.LatLng import LatLng
from alt_lk.data.AltFile import AltFile
from alt_lk.data.GeoTIFFFile import GeoTIFFFile
from utils_future import SparseArrayFile

log = Log('Alt')


@dataclass
class Alt:
    alt_m: float

    def __str__(self):
        return f'{self.alt_m:,.0f}m / {self.alt_ft:,.0f}ft'

    FEET_PER_METER = 3.28084

    @property
    def alt_ft(self) -> float:
        return self.alt_m * Alt.FEET_PER_METER

    MIN_LATLNG = LatLng(5, 78)
    MAX_LATLNG = LatLng(9, 82)
    BBOX = BBox(MIN_LATLNG, MAX_LATLNG)
    MIN_LAT = MIN_LATLNG.lat
    MAX_LAT = MAX_LATLNG.lat
    LAT_SPAN = MAX_LAT - MIN_LAT
    MIN_LNG = MIN_LATLNG.lng

    COMBINED_DATA_FILE_PATH = os.path.join('data', 'alt.combined.lk.npz')
    COMBINED_DATA_FILE = SparseArrayFile(COMBINED_DATA_FILE_PATH)

    @staticmethod
    @cache
    def get_alt_data_for_lk():
        # filed
        if Alt.COMBINED_DATA_FILE.exists:
            return Alt.COMBINED_DATA_FILE.read()

        # not filed
        data = AltFile.get_combined_data(Alt.BBOX)
        Alt.COMBINED_DATA_FILE.write(data)
        return data

    @staticmethod
    @cache
    def latlng_to_indices(latlng: LatLng):
        lat, lng = latlng.tuple
        i_lat = (Alt.LAT_SPAN + 1) * GeoTIFFFile.DIM - int(
            (lat - Alt.MIN_LAT) * GeoTIFFFile.DIM
        )
        i_lng = int((lng - Alt.MIN_LNG) * GeoTIFFFile.DIM)

        return (i_lat, i_lng)

    @staticmethod
    @cache
    def from_latlng(latlng: LatLng) -> float:
        data = Alt.get_alt_data_for_lk()
        (i_lat, i_lng) = Alt.latlng_to_indices(latlng)
        return Alt(data[i_lat][i_lng])
