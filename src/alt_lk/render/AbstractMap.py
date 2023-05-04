import json
import os
from functools import cached_property

from PIL import Image
from utils import Log, hashx

log = Log('basic_map')
MIN_ALT, MAX_ALT = 0, 2524


def get_color_default(value):
    if value > 0:
        return (0, 128, 0)
    return (0, 32, 64)


class AbstractMap:
    def __init__(self, data, get_color=None):
        self.data = data
        self.get_color = get_color or get_color_default

    @cached_property
    def label(self):
        return hashx.md5(json.dumps(self.data.tolist()))[:3].upper()

    @property
    def png_path(self):
        return os.path.join(
            'images', f'{self.__class__.__name__}.{self.label}.png'
        )

    def write(self):
        data = self.data
        dim_x, dim_y = len(data[0]), len(data)
        img = Image.new('RGB', (dim_x, dim_y))
        pixels = img.load()
        for x in range(dim_x):
            for y in range(dim_y):
                pixels[x, y] = self.get_color(data[y][x])

        img.save(self.png_path)
        log.info(f'Wrote {self.png_path}')
