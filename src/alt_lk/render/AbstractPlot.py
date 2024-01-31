import os

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
from utils import Log

log = Log('AbstractPlot')


class AbstractPlot:
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

    @staticmethod
    def set_tight_layout():
        plt.tight_layout()

    @staticmethod
    def save_and_start(image_path: str):
        plt.savefig(image_path, dpi=AbstractPlot.DPI)
        log.info(f'Wrote {image_path}.')
        os.startfile(image_path)
        plt.close()

    def write(self, image_path: str):
        self.build_plot()
        self.set_tight_layout()
        self.save_and_start(image_path)
