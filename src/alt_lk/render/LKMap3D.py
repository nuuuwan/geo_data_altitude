import matplotlib.pyplot as plt
import numpy as np

from alt_lk.alt.Alt import Alt
from alt_lk.core import BBox
from alt_lk.render.AbstractPlot import AbstractPlot


class LKMap3D(AbstractPlot):
    def __init__(self, bbox: BBox):
        self.bbox = bbox

    def build_plot(self):
        data = Alt.get_matrix_subset(self.bbox)
        alt = np.array(data)
        lat, lng = np.mgrid[: alt.shape[0], : alt.shape[1]]

        ax = plt.axes(projection='3d')
        ax.plot_surface(
            lat,
            lng,
            alt,
            cmap=self.cmap,
        )
        ax.set_xlabel('y')
        ax.set_ylabel('x')
        ax.set_zlabel('alt')
