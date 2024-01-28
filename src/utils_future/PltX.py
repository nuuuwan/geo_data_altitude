import os

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from utils import Log

log = Log('examples')


def get_cmap():
    colors = ["darkgreen", "green", "yellow", "orange", "red", "brown"]
    cmap = mcolors.LinearSegmentedColormap.from_list('custom', colors)
    return cmap


CMAP = get_cmap()


class PltX:
    DPI = 2_400

    @staticmethod
    def get_image_path(py_path: str, label: str = ""):
        base_name = os.path.basename(py_path)
        image_path = os.path.join('examples','images', f'{base_name}{label}.png')
        return image_path

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
        plt.savefig(image_path, dpi=PltX.DPI)
        log.info(f'Wrote {image_path}.')
        os.startfile(image_path)
        plt.close()

        image_path_unix = image_path.replace('\\', '/') 

        print(
            f'''
### [{base_name}](examples/{base_name})

![{base_name}]({image_path_unix})
        '''
        )


    @staticmethod
    def write(py_file_name: str, label: str = ""):
        image_path = PltX.get_image_path(py_file_name, label)
        PltX.remove_axes()
        PltX.set_tight_layout()
        PltX.save_and_start(image_path)

        