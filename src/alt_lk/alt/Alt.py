from functools import cache

from alt_lk.core.BBox import BBox
from alt_lk.core.LatLng import LatLng
from alt_lk.data.GeoTIFFFile import GeoTIFFFile
from alt_lk.data.JSONAltFile import JSONAltFile


class Alt:
    MIN_LATLNG = LatLng(5, 78)
    MAX_LATLNG = LatLng(9, 82)
    BBOX = BBox(MIN_LATLNG, MAX_LATLNG)
    MIN_LAT = MIN_LATLNG.lat
    MAX_LAT = MAX_LATLNG.lat
    LAT_SPAN = MAX_LAT - MIN_LAT
    MIN_LNG = MIN_LATLNG.lng

    @staticmethod
    @cache
    def get_combined_data_for_lk():
        return JSONAltFile.get_combined_data(Alt.BBOX)

    @staticmethod
    @cache
    def latlng_to_indices(latlng: tuple[int, int]):
        lat, lng = latlng
        i_lat = (Alt.LAT_SPAN + 1) * GeoTIFFFile.DIM - int(
            (lat - Alt.MIN_LAT) * GeoTIFFFile.DIM
        )
        i_lng = int((lng - Alt.MIN_LNG) * GeoTIFFFile.DIM)

        return (i_lat, i_lng)

    @staticmethod
    @cache
    def from_latlng(latlng: tuple[int, int]):
        data = Alt.get_combined_data_for_lk()
        (i_lat, i_lng) = Alt.latlng_to_indices(latlng)
        return data[i_lat][i_lng]
