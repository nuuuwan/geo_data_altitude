import os
from functools import cache, cached_property

import numpy as np
from utils import JSONFile, Log

from alt_lk.data.GeoTIFFFile import GeoTIFFFile

log = Log('JSONAltFile')


class JSONAltFile(JSONFile):
    DIR_JSON_ALT = os.path.join('data', 'json')
    MIN_LAT = 5
    MAX_LAT = 9
    MIN_LNG = 78
    MAX_LNG = 82
    LAT_SPAN = MAX_LAT - MIN_LAT
    LNG_SPAN = MAX_LNG - MIN_LNG

    def __init__(self, path):
        self.path = path

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
        return os.path.join(JSONAltFile.DIR_JSON_ALT,
                            f'alt.{lat:03d}N.{lng:03d}E.json')

    @staticmethod
    def from_latlng(latlng: tuple[int, int]):
        return JSONAltFile(JSONAltFile.get_path_from_latlng(latlng))

    @staticmethod
    def get_empty_data() -> list[list[float]]:
        return np.array([[0] * GeoTIFFFile.DIM] * GeoTIFFFile.DIM)

    @staticmethod
    def from_geotiff(geotiff: GeoTIFFFile):
        data = geotiff.data
        log.debug(f'Read {geotiff.path}.')
        json_alt_file = JSONAltFile.from_latlng(geotiff.latlng)
        json_alt_file.write(data)
        log.info(f'Wrote {json_alt_file}.')
        return json_alt_file

    @staticmethod
    def list_from_dir_geotiff(dir_geotiff: str):
        json_alt_file_list = []
        for file_name in os.listdir(dir_geotiff):
            if not file_name.endswith('_3arc_v2.tif'):
                continue
            path = os.path.join(dir_geotiff, file_name)
            geotiff = GeoTIFFFile(path)
            json_alt_file = JSONAltFile.from_geotiff(geotiff)
            json_alt_file_list.append(json_alt_file)
        return json_alt_file_list

    @staticmethod
    @cache
    def get_combined_data(min_lat, max_lat, min_lng, max_lng):
        matrix_block = []
        for lat in range(max_lat, min_lat - 1, -1):
            matrix_row = []
            for lng in range(min_lng, max_lng + 1):
                json_alt_file = JSONAltFile.from_latlng((lat, lng))
                if os.path.exists(json_alt_file.path):
                    matrix = np.array(json_alt_file.read())
                    log.debug(f'Read {json_alt_file}')
                else:
                    matrix = JSONAltFile.get_empty_data()
                    log.warning(f'No JSONAltFile for {lat},{lng}')
                dim_x = len(matrix)
                dim_y = len(matrix[0])
                assert dim_x == dim_y == GeoTIFFFile.DIM

                matrix_row.append(matrix)
            matrix_block.append(matrix_row)
        matrix_block = np.block(matrix_block)
        data = matrix_block.tolist()
        dim_x = len(data)
        dim_y = len(data[0])
        log.debug(f'dim_x={dim_x:,}, dim_y={dim_y:,}')
        return data

    @staticmethod
    @cache
    def get_combined_data_for_lk():
        return JSONAltFile.get_combined_data(
            JSONAltFile.MIN_LAT,
            JSONAltFile.MAX_LAT,
            JSONAltFile.MIN_LNG,
            JSONAltFile.MAX_LNG
        )
