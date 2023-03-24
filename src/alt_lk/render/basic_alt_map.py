from functools import cache

from PIL import Image
from utils import Log

from alt_lk import AltIdx

log = Log('BasicAltMap')


class BasicAltMap:
    @staticmethod
    def get_color(alt):
        for min_alt, color in [
            [2000, (255, 0, 0)],
            [1000, (255, 125, 0)],
            [500, (255, 255, 0)],
            [250, (0, 128, 0)],
            [0, (0, 255, 0)],
        ]:
            if alt > min_alt:
                return color
        return (0, 255, 128)

    def __init__(
        self,
        min_latlng: tuple[float, float],
        max_latlng: tuple[float, float],
        incr: float,
    ):
        self.min_latlng = min_latlng
        self.max_latlng = max_latlng
        self.incr = incr

    @property
    def path(self):
        return 'images/basic_alt_map.png'

    @cache
    def get_matrix(self):
        min_lat, min_lng = self.min_latlng
        max_lat, max_lng = self.max_latlng
        lat = min_lat
        matrix = []
        while lat < max_lat:
            lng = min_lng
            row = []
            while lng < max_lng:
                alt = AltIdx.get((lat, lng))
                row.append(alt)
                print(lat, lng, alt, end='\r')
                lng += self.incr
            matrix.append(row)
            lat += self.incr
        return matrix

    def draw(self):
        matrix = self.get_matrix()
        width, height = len(matrix[0]), len(matrix)
        img = Image.new('RGB', (width, height), color='white')
        pixels = img.load()
        for x in range(width):
            for y in range(height):
                alt = matrix[y][x]
                color = BasicAltMap.get_color(alt)
                pixels[x, y] = color
        img.save(self.path)
        log.debug(f'Saved {self.path}')


if __name__ == '__main__':
    BasicAltMap((6, 79), (10, 81), 0.1).draw()
