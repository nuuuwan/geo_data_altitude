from functools import cache

from alt_lk.data.GeoTIFFFile import GeoTIFFFile
from alt_lk.data.JSONAltFile import JSONAltFile


class Alt:
    @staticmethod
    @cache
    def latlng_to_indices(latlng: tuple[int, int]):
        lat, lng = latlng
        i_lat = (JSONAltFile.LAT_SPAN + 1) * GeoTIFFFile.DIM - int(
            (lat - JSONAltFile.MIN_LAT) * GeoTIFFFile.DIM
        )
        i_lng = int((lng - JSONAltFile.MIN_LNG) * GeoTIFFFile.DIM)

        # i_lat = 6005 - int((lat - 5) * DIM)
        # i_lng = int((lng - 78) * DIM)

        return (i_lat, i_lng)

    @staticmethod
    @cache
    def from_latlng(latlng: tuple[int, int]):
        data = JSONAltFile.get_combined_data_for_lk()
        (i_lat, i_lng) = Alt.latlng_to_indices(latlng)
        return data[i_lat][i_lng]
