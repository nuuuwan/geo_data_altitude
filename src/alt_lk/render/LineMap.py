import json
import os
from functools import cached_property

from utils import Log, hashx
from utils.xmlx import _

from alt_lk._utils_future.ImageConvert import ImageConvert
from alt_lk.compute._constants import DIM_X, DIM_Y, MAX_ALT

log = Log('LineMap')


class LineMap:
    def __init__(self, line_info_list, get_color=None, label_info_list=None):
        self.line_info_list = line_info_list
        self.get_color = get_color
        self.label_info_list = label_info_list or []

    @cached_property
    def label(self):
        return hashx.md5(json.dumps(self.line_info_list))[:3].upper()

    @property
    def svg_path(self):
        return os.path.join(
            'images', f'{self.__class__.__name__}.{self.label}.svg'
        )

    def render_line(self, line_info):
        x = line_info['x']
        y1 = line_info['y1']
        y2 = line_info['y2']
        distance = line_info['distance']
        color = self.get_color(distance)

        width = 20
        x_left = x - width / 2
        y_top = y1
        height = y2 - y1

        return _(
            'rect',
            None,
            dict(
                x=x_left,
                y=y_top,
                width=width,
                height=height,
                fill=color,
            ),
        )

    def render_label(self, label_info):
        DEFAULT_FONT_SIZE = 15
        x, y = label_info['xy']
        name = label_info['name']
        label = name
        alt = label_info.get('alt')
        if alt:
            label += f' ({alt:.0f}m)'
            font_size = DEFAULT_FONT_SIZE * max(1, alt * 2 / MAX_ALT)
        else:
            font_size = DEFAULT_FONT_SIZE
        text_angle = -90
        transform = ' '.join(
            [
                f'translate({x},{y})',
                f'rotate({text_angle})',
                f'translate({-x},{-y})',
            ]
        )

        return _(
            'text',
            label,
            dict(
                x=x,
                y=y,
                fill='black',
                font_size=font_size,
                font_family='Tahoma',
                text_anchor='start',
                transform=transform,
            ),
        )

    def render_sky(self):
        return _(
            'rect',
            None,
            dict(x=0, y=0, width=DIM_X, height=DIM_Y, fill='#1b7ced'),
        )

    def render_lines(self):
        return list(
            map(
                self.render_line,
                sorted(
                    self.line_info_list,
                    key=lambda d: d['distance'],
                    reverse=True,
                ),
            )
        )

    def render_labels(self):
        return list(map(self.render_label, self.label_info_list))

    def render(self):
        return _(
            'svg',
            [self.render_sky()] + self.render_lines() + self.render_labels(),
            dict(width=DIM_X, height=DIM_Y),
        )

    def write(self):
        n = len(self.line_info_list)
        log.debug(f'Writing LineMap ({n:,} lines)')
        svg = self.render()
        svg.store(self.svg_path)
        log.info(f'Wrote {self.svg_path}')
        png_path = ImageConvert(self.svg_path).to_png()
        os.startfile(os.path.realpath(png_path))
