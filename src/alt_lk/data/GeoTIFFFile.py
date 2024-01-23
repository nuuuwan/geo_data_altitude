import os
from functools import cached_property

import rasterio
from utils import Log

from alt_lk.core.LatLng import LatLng
from utils_future import File

log = Log('GeoTIFFFile')


class GeoTIFFFile(File):
    DIM = 1201
    DIR_ALT_TIF = os.path.join('data', 'geo-tiff')

    @cached_property
    def latlng(self) -> LatLng:
        file_name = os.path.basename(self.path)
        lat = int(file_name[1:3])
        lng = int(file_name[5:8])
        return LatLng(lat, lng)

    @staticmethod
    def get_path_from_latlng(latlng: LatLng):
        lat, lng = LatLng.tuple
        return os.path.join(GeoTIFFFile.DIR_ALT_TIF,
                            f'n{lat:02d}_e{lng:03d}_3arc_v2.tif')

    @staticmethod
    def from_latlng(latlng: LatLng):
        return GeoTIFFFile(GeoTIFFFile.get_path_from_latlng(latlng))

    @cached_property
    def data(self) -> list[list[float]]:
        if not os.path.exists(self.path):
            raise FileNotFoundError

        data = None
        with rasterio.open(self.path) as src:
            data = src.read(1).tolist()
        dim_x = len(data)
        dim_y = len(data[0])
        assert dim_x == dim_y == GeoTIFFFile.DIM
        return data
