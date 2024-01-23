import os
from functools import cache

import numpy as np
from utils import Log

from alt_lk.core.BBox import BBox
from alt_lk.core.LatLng import LatLng
from alt_lk.data.GeoTIFFFile import GeoTIFFFile
from utils_future import SparseArrayFile

log = Log('AltFile')


class AltFile(SparseArrayFile):
    DIR_ALT = os.path.join('data', 'alt')

    @staticmethod
    def get_path_from_latlng(latlng: LatLng):
        return os.path.join(AltFile.DIR_ALT,
                            f'alt.{latlng.str_03d}.npz')

    @staticmethod
    def from_latlng(latlng: LatLng):
        return AltFile(AltFile.get_path_from_latlng(latlng))

    @staticmethod
    def get_empty_data() -> list[list[float]]:
        return np.array([[0] * GeoTIFFFile.DIM] * GeoTIFFFile.DIM)

    @staticmethod
    def from_geotiff(geotiff: GeoTIFFFile):
        data = geotiff.data
        json_alt_file = AltFile.from_latlng(geotiff.latlng)
        if not os.path.exists(AltFile.DIR_ALT):
            os.makedirs(AltFile.DIR_ALT)
            log.info(f'Created {AltFile.DIR_ALT}.')

        json_alt_file.write(data)
        return json_alt_file

    @staticmethod
    def list_from_dir_geotiff(dir_geotiff: str):
        json_alt_file_list = []
        for file_name in os.listdir(dir_geotiff):
            if not file_name.endswith('_3arc_v2.tif'):
                continue
            path = os.path.join(dir_geotiff, file_name)
            geotiff = GeoTIFFFile(path)
            json_alt_file = AltFile.from_geotiff(geotiff)
            json_alt_file_list.append(json_alt_file)
        return json_alt_file_list

    @staticmethod
    @cache
    def get_combined_data(bbox: BBox):
        min_latlng, max_latlng = bbox.tuple
        min_lat, min_lng = min_latlng.tuple
        max_lat, max_lng = max_latlng.tuple

        matrix_block = []
        for lat in range(max_lat, min_lat - 1, -1):
            matrix_row = []
            for lng in range(min_lng, max_lng + 1):
                json_alt_file = AltFile.from_latlng(LatLng(lat, lng))
                if os.path.exists(json_alt_file.path):
                    matrix = np.array(json_alt_file.read())
                else:
                    matrix = AltFile.get_empty_data()
                    log.warning(f'No AltFile for {lat},{lng}')
                dim_x = len(matrix)
                dim_y = len(matrix[0])
                assert dim_x == dim_y == GeoTIFFFile.DIM

                matrix_row.append(matrix)
            matrix_block.append(matrix_row)
        matrix_block = np.block(matrix_block)
        data = matrix_block.tolist()
        dim_x = len(data)
        dim_y = len(data[0])
        assert dim_x == GeoTIFFFile.DIM * (max_lat - min_lat + 1)
        assert dim_y == GeoTIFFFile.DIM * (max_lng - min_lng + 1)

        return data
