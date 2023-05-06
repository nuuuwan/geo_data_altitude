import json
import os
from functools import cached_property

import svgpathtools
from utils import Log, hashx
from utils.xmlx import _

from alt_lk._utils_future.ImageConvert import ImageConvert
from alt_lk.compute._constants import DIM_X, DIM_Y

log = Log('LineMap')


def smooth_path(d):
    try:
        path = svgpathtools.parse_path(d)
        smoothed_path = svgpathtools.smoothed_path(
            path,
        )
        return smoothed_path.d()
    except BaseException:
        log.error(f'Failed to smooth path: {d}')
        return d


class PathMap:
    def __init__(self, group_to_line, get_color):
        self.group_to_line = group_to_line
        self.get_color = get_color

    @cached_property
    def label(self):
        return hashx.md5(json.dumps(self.group_to_line))[:3].upper()

    @property
    def svg_path(self):
        return os.path.join(
            'images', f'{self.__class__.__name__}.{self.label}.svg'
        )

    def render_path(self, item):
        WINDOW = 10

        group, lines = item
        if len(lines) <= WINDOW * 2 + 1:
            return None
        lines = sorted(lines, key=lambda d: d[0])
        n = len(lines)
        avg_lines = []
        for i in range(WINDOW, n - WINDOW):
            avg_lines.append(
                (
                    lines[i][0],
                    sum([y for x, y in lines[i - WINDOW: i + WINDOW + 1]])
                    / (WINDOW * 2 + 1),
                )
            )

        d_list = []
        for x, y in avg_lines + [avg_lines[0]]:
            if not d_list:
                d_list.append(f'M{x},{y}')
            else:
                d_list.append(f'L{x},{y}')

        d = ' '.join(d_list)
        # smoothed_d = smooth_path(d)
        color = self.get_color(int(group) * 5)
        return _(
            'path',
            None,
            dict(
                d=d,
                fill=color,
                stroke='black',
                stroke_width=1,
            ),
        )

    def render_paths(self):
        rendered_paths = []
        for item in sorted(
            self.group_to_line.items(), key=lambda item: item[0]
        ):
            rendered_path = self.render_path(item)
            if rendered_path:
                rendered_paths.append(rendered_path)
        return rendered_paths

    def render_sky(self):
        return _(
            'rect',
            None,
            dict(x=0, y=0, width=DIM_X, height=DIM_Y, fill='#1b7ced'),
        )

    def write(self):
        svg = _(
            'svg',
            [self.render_sky()] + self.render_paths(),
            dict(width=DIM_X, height=DIM_Y),
        )
        svg.store(self.svg_path)
        log.info(f'Wrote {self.svg_path}')

        png_path = ImageConvert(self.svg_path).to_png()
        os.startfile(os.path.realpath(png_path))
