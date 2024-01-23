import os
from functools import cached_property

import rasterio
from utils import File, Log

log = Log('GeoTIFFFile')


class GeoTIFFFile(File):
    DIM = 1201
    DIR_GEOTIFF = os.path.join('data', 'tif')

    @cached_property 
    def latlng(self) -> tuple[float, float]:
        file_name = os.path.basename(self.path)
        lat = int(file_name[1:3])
        lng = int(file_name[5:8])
        return (lat, lng)

    def __str__(self) -> str:
        return f'{self.path} ({self.size_m:.2f}MB)'

    @cached_property
    def size(self) -> int:
        return os.path.getsize(self.path)

    @cached_property
    def size_m(self) -> float:
        return self.size / 1024 / 1024

    @staticmethod
    def get_path_from_latlng(latlng: tuple[int, int]):
        lat, lng = latlng
        # TODO: add "alt"
        return os.path.join(GeoTIFFFile.DIR_GEOTIFF, f'n{lat:02d}_e{lng:03d}_3arc_v2.tif')

    @staticmethod
    def from_latlng(latlng: tuple[int, int]):
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
