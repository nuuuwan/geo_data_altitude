import os

import rasterio
from utils import Log

log = Log('GeoTIFFFile')


class GeoTIFFFile:
    @staticmethod
    def empty_data():
        DIM = 1201
        return [[0] * DIM] * DIM

    def __init__(self, latlng: tuple[int, int]):
        self.latlng = latlng

    @property
    def path(self) -> str:
        lat, lng = self.latlng
        return f'data/tif/n{lat:02d}_e{lng:03d}_3arc_v2.tif'

    def get_data(self):
        data = None
        if not os.path.exists(self.path):
            log.warning(
                f'File not found: {self.path}. Returning empty matrix.'
            )
            return GeoTIFFFile.empty_data()

        with rasterio.open(self.path) as src:
            data = src.read(1).tolist()
        return data
