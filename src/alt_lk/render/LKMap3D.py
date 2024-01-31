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
        
        # dim_lat, dim_lng = alt.shape
        # lat = lat / dim_lat * self.bbox.lat_span - self.bbox.max_lat
        # lng = lng / dim_lng * self.bbox.lng_span + self.bbox.min_lng
        
        ax = plt.axes(projection='3d')
        ax.plot_surface(
            lat,
            lng,
            alt,
            cmap=self.cmap,
        )
        ax.view_init(azim=-45, elev=67.5)
        ax.set_xlabel('lat')
        ax.set_ylabel('lng')
        ax.set_zlabel('alt')
