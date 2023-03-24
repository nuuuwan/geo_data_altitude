from functools import cache, cached_property

from utils import JSONFile


class AltIdx:
    BASE_URL = 'https://raw.githubusercontent.com/nuuuwan/alt_lk/main/data'

    def __init__(self, idx_latlng: tuple[float, float]):
        self.idx_latlng = idx_latlng

    def from_latlng(latlng: tuple[float, float]):
        lat, lng = latlng
        return AltIdx((int(lat) + 1, int(lng)))

    @cached_property
    def max_lat(self):
        return self.idx_latlng[0]

    @cached_property
    def min_lng(self):
        return self.idx_latlng[1]

    @cached_property
    def min_lat(self):
        return self.max_lat - 1

    @cached_property
    def max_lng(self):
        return self.min_lng + 1

    @cache
    def is_included(self, latlng: tuple[float, float]) -> bool:
        lat, lng = latlng
        return (
            self.min_lat <= lat < self.max_lat
            and self.min_lng <= lng < self.max_lng
        )

    @cached_property
    def local_path(self) -> str:
        return f'data/{self.max_lat-1:02d}.{self.min_lng:02d}.json'

    @cached_property
    def matrix(self) -> list:
        json_data = JSONFile(self.local_path).read()
        return json_data['matrix']

    @cache
    def _get(self, latlng: tuple[float, float]) -> float:
        if not self.is_included(latlng):
            return None

        matrix = self.matrix
        dim_x = len(matrix)
        dim_y = len(matrix[0])

        lat, lng = latlng
        i_x = int((lng - self.min_lng) * dim_x)
        i_y = int((lat - self.min_lat) * dim_y)

        return matrix[i_x][i_y]

    @staticmethod
    def get(latlng: tuple[float, float]) -> float:
        alt_idx = AltIdx.from_latlng(latlng)
        return alt_idx._get(latlng)
