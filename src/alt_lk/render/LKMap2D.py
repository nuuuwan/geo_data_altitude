import matplotlib.pyplot as plt
import numpy as np

from alt_lk.alt.Alt import Alt
from alt_lk.core import BBox
from alt_lk.render.AbstractPlot import AbstractPlot


class LKMap2D(AbstractPlot):
    def __init__(self, bbox: BBox):
        self.bbox = bbox

    def build_plot(self):
        data = Alt.get_matrix_subset(self.bbox)
        arr = np.array(data)

        arr[arr <= 0] = -1

        plt.imshow(arr, cmap=self.cmap)
        plt.colorbar()
