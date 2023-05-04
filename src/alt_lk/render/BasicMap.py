import colorsys
import os

import cv2
import imageio
from PIL import Image
from utils import Log

from alt_lk.core.JSONAltFile import JSONAltFile

log = Log('basic_map')
MIN_ALT, MAX_ALT = 0, 2524


class BasicMap:
    def __init__(self, mid_alt):
        self.mid_alt = mid_alt
        log.debug(f'BasicMap(mid_alt={mid_alt})')

    def get_color(self, alt):
        if alt <= 0:
            return (0, 64, 128)

        if alt > self.mid_alt:
            palt = (alt - self.mid_alt) / (MAX_ALT - self.mid_alt)
            h = (int)(120 * (1 - palt))
        else:
            palt = (alt - MIN_ALT) / (self.mid_alt - MIN_ALT)
            h = 120 + (int)(120 * (1 - palt))

        s, light = 100, 33
        (r, g, b) = colorsys.hls_to_rgb(h / 360, light / 100, s / 100)
        return (int)(r * 255), (int)(g * 255), (int)(b * 255)

    def write(self):
        png_path = f'images/all.{self.mid_alt}.png'
        if os.path.exists(png_path):
            log.debug(f'{png_path} exists')
            return png_path

        data = JSONAltFile().read()
        dim_x, dim_y = len(data[0]), len(data)
        img = Image.new('RGB', (dim_x, dim_y))
        pixels = img.load()
        for x in range(dim_x):
            for y in range(dim_y):
                pixels[x, y] = self.get_color(data[y][x])

        img.save(png_path)
        log.info(f'Wrote {png_path}')
        return png_path

    @staticmethod
    def create_animated_gif():
        MAX_ALT = 2524
        images = []
        for i in range(0, 15):
            mid_alt = int(MAX_ALT / (2 ** (i / 2)))
            image_path = BasicMap(mid_alt).write()
            image = imageio.imread(image_path)
            image = cv2.resize(image, (800, 1000))

            images.append(image)
        # mirror
        n = len(images)
        for i in range(n):
            images.append(images[n - i - 1])

        gif_path = 'images/all.gif'
        imageio.mimsave(gif_path, images, duration=0.2)
        log.info(f'Wrote {gif_path}')


if __name__ == '__main__':
    BasicMap.create_animated_gif()
