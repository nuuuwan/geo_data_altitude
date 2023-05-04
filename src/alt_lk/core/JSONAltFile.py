import colorsys
import math
import os

from utils import JSONFile, Log

from alt_lk.core.GeoTIFFFile import GeoTIFFFile

log = Log('JSONAltFile')

DIM = 1201
MIN_ALT, MAX_ALT = 0, 2524
MIN_LAT, MIN_LNG, MAX_LAT, MAX_LNG = 5, 78, 10, 82


def get_color(alt):
    if alt <= MIN_ALT:
        return (0, 64, 128)
    if alt > MAX_ALT:
        return (128, 0, 0)

    palt = math.sqrt(alt / MAX_ALT)
    h = (int)(120 * (1 - palt))
    s, light = 100, 33
    (r, g, b) = colorsys.hls_to_rgb(h / 360, light / 100, s / 100)
    return (int)(r * 255), (int)(g * 255), (int)(b * 255)


class JSONAltFile:
    @property
    def path(self):
        return 'data/lk.json'

    def read(self):
        if os.path.exists(self.path):
            return JSONFile(self.path).read()

        return self.read_from_tifs()

    def write(self, data):
        JSONFile(self.path).write(data)
        dim_x, dim_y = len(data), len(data[0])
        log.info(f'Wrote {self.path} ({dim_x} x {dim_y})')
        return self.path

    def read_from_tifs(self):
        log.debug('Reading from TIF data...')
        n_lat, n_lng = MAX_LAT - MIN_LAT, MAX_LNG - MIN_LNG
        data = [[0 for _ in range(n_lng * DIM)] for _ in range(n_lat * DIM)]

        for i_lat in range(n_lat):
            for i_lng in range(n_lng):
                tif = GeoTIFFFile((MIN_LAT + i_lat, MIN_LNG + i_lng))
                item_data = tif.get_data()
                if not item_data:
                    continue
                for ii_y in range(DIM):
                    i_y = (n_lat - i_lat - 1) * DIM + ii_y
                    for ii_x in range(DIM):
                        i_x = i_lng * DIM + ii_x
                        data[i_y][i_x] = item_data[ii_y][ii_x]

        self.write(data)
        log.debug(f'Wrote {self.path}')
        return data
