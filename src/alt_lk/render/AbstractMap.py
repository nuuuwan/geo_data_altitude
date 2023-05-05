import json
import os
from functools import cached_property

from PIL import Image, ImageDraw, ImageFont
from utils import Log, hashx

log = Log('basic_map')
MIN_ALT, MAX_ALT = 0, 2524


def get_color_default(value):
    if value > 0:
        return (0, 128, 0)
    return (0, 32, 64)


class AbstractMap:
    def __init__(self, data, get_color=None, label_info_list=None):
        self.data = data
        self.get_color = get_color or get_color_default
        self.label_info_list = label_info_list or []

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

        # colors
        pixels = img.load()
        for x in range(dim_x):
            for y in range(dim_y):
                val = data[y][x]
                color = self.get_color(val)

                pixels[x, y] = color

        # labels
        FONT_SIZE = 15
        font = ImageFont.truetype('arial.ttf', FONT_SIZE)

        draw = ImageDraw.Draw(img)
        for label_info in self.label_info_list:
            x, y = label_info['xy']
            name = label_info['name']
            draw.text((x, y), name, (0, 0, 0), font=font)

            alt = label_info.get('alt')

            if alt is not None:
                label = f'{alt}m'
                draw.text(
                    (x + FONT_SIZE, y + FONT_SIZE * 1.1),
                    label,
                    (0, 0, 0),
                    font=font,
                )

        img.save(self.png_path)
        log.info(f'Wrote {self.png_path}')

        os.startfile(os.path.realpath(self.png_path))
