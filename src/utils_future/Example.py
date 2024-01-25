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


class Example:
    DPI = 2_400

    @staticmethod
    def write(arr: np.array, py_file_name: str):
        plt.imshow(arr, cmap=CMAP)
        plt.colorbar()

        base_name = os.path.basename(py_file_name)
        image_path = os.path.join('examples', f'{base_name}.png')

        ax = plt.gca()
        # Hide grid lines
        ax.grid(False)

        # Hide axes ticks
        ax.set_xticks([])
        ax.set_yticks([])

        plt.tight_layout()
        plt.savefig(image_path, dpi=Example.DPI)
        log.info(f'Wrote {image_path}.')
        os.startfile(image_path)
        plt.close()

        print(
            f'''
### [{base_name}](examples/{base_name})

![{base_name}](examples/{base_name}.png)
        '''
        )
