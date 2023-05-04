import os

from PIL import Image
from utils import Log

from alt_lk.data.JSONCombinedAltFile import JSONCombinedAltFile

log = Log('basic_map')
MIN_ALT, MAX_ALT = 0, 2524


class AbstractAltMap:
    def get_color(self, alt):
        raise NotImplementedError()

    @property
    def label(self):
        return self.__class__.__name__

    def write(self):
        png_path = f'images/all.{self.label}.png'
        if os.path.exists(png_path):
            log.debug(f'{png_path} exists')
            return png_path

        data = JSONCombinedAltFile().read()
        dim_x, dim_y = len(data[0]), len(data)
        img = Image.new('RGB', (dim_x, dim_y))
        pixels = img.load()
        for x in range(dim_x):
            for y in range(dim_y):
                pixels[x, y] = self.get_color(data[y][x])

        img.save(png_path)
        log.info(f'Wrote {png_path}')
        return png_path
