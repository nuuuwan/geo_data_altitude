import colorsys

from alt_lk.render.AbstractAltMap import AbstractAltMap

MIN_ALT, MAX_ALT = 0, 2524


class MidAltMap(AbstractAltMap):
    def __init__(self, mid_alt):
        self.mid_alt = mid_alt

    @property
    def label(self):
        return f'MidAltMap.{self.mid_alt}'

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


if __name__ == '__main__':
    MidAltMap(600).write()
