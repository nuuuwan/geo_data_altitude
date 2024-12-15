import os

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from utils import Log

from alt_lk.core import BBox

log = Log('AbstractPlot')


class AbstractPlot:
    def __init__(self, bbox: BBox):
        self.bbox = bbox

    DPI = 600

    def build_plot(self):
        raise NotImplementedError

    @property
    def cmap(self):
        cmap = mcolors.LinearSegmentedColormap.from_list(
            'custom',
            ["darkgreen", "green", "yellow", "orange", "red", "brown"],
        )
        return cmap

    @staticmethod
    def remove_axes():
        ax = plt.gca()
        ax.grid(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.axis('off'),
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)

    @staticmethod
    def set_tight_layout():
        plt.tight_layout()

    @staticmethod
    def save_and_start(image_path: str):
        plt.savefig(image_path, dpi=AbstractPlot.DPI)
        log.info(f'Wrote {image_path}.')
        # os.startfile(image_path)

    def write(self, place: str, image_path: str, force: bool = False):
        if not force and os.path.exists(image_path):
            log.info(f'Already exists: {image_path}')
            return
        plt.size = (8, 9)
        # plt.title(place)
        self.remove_axes()
        self.build_plot()
        self.set_tight_layout()
        self.save_and_start(image_path)
        plt.close()
