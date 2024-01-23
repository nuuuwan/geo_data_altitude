from functools import cache

from alt_lk.data.AltFile import AltFile
from alt_lk.data.GeoTIFFFile import GeoTIFFFile


class Alt:
    @staticmethod
    @cache
    def latlng_to_ij(latlng: tuple[int, int]):
        lat, lng = latlng
        i = int((lat - AltFile.MIN_LAT) * GeoTIFFFile.DIM)
        j = int((lng - AltFile.MIN_LNG) * GeoTIFFFile.DIM)
        return (i, j)

    @staticmethod
    @cache
    def from_latlng(latlng: tuple[int, int]):
        data = AltFile.get_combined_data_for_lk()
        (i, j) = Alt.latlng_to_ij(latlng)
        return data[i][j]
