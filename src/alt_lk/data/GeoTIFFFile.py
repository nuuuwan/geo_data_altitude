import os
from functools import cached_property

import numpy as np
import rasterio
from utils import Log

from alt_lk.core.LatLng import LatLng
from alt_lk.core.Resolution import Resolution
from utils_future import File

log = Log('GeoTIFFFile')


class GeoTIFFFile(File):
    DIR_GEO_TIF = os.path.join('data', 'geo-tiff-local-only')
    DIR_GEO_TIF_ARC3 = os.path.join(DIR_GEO_TIF, '3arc_v2')
    DIR_GEO_TIF_ARC1 = os.path.join(DIR_GEO_TIF, '1arc_v3')

    @cached_property
    def latlng(self) -> LatLng:
        file_name = os.path.basename(self.path)
        lat = int(file_name[1:3])
        lng = int(file_name[5:8])
        return LatLng(lat, lng)

    @cached_property
    def resolution(self) -> Resolution:
        file_name = os.path.basename(self.path)
        arc_seconds = int(file_name[9:10])
        version = int(file_name[15:16])
        return Resolution(arc_seconds, version)

    @staticmethod
    def get_path_from_latlng_and_resolution(
        latlng: LatLng, resolution: Resolution
    ):
        lat, lng = latlng.tuple
        return os.path.join(
            GeoTIFFFile.DIR_ALT_TIF,
            resolution.file_code,
            f'n{lat:02d}_e{lng:03d}_{resolution.file_code}.tif',
        )

    @staticmethod
    def from_latlng_and_resolution(latlng: LatLng, resolution: Resolution):
        return GeoTIFFFile(
            GeoTIFFFile.get_path_from_latlng(latlng, resolution)
        )

    @cached_property
    def data(self) -> np.array:
        if not os.path.exists(self.path):
            raise FileNotFoundError

        data = None
        with rasterio.open(self.path) as src:
            data = src.read(1).tolist()
        dim_x = len(data)
        dim_y = len(data[0])
        assert dim_x == dim_y == self.resolution.dim1
        return np.array(data)
