import matplotlib.pyplot as plt
import numpy as np

from alt_lk.alt.Alt import Alt
from alt_lk.render.AbstractPlot import AbstractPlot


class Map3D(AbstractPlot):
    def build_plot(self):
        self.remove_axes()

        alt = Alt.get_matrix_subset(self.bbox)
        lat, lng = np.mgrid[: alt.shape[0], : alt.shape[1]]

        dim_lat, dim_lng = alt.shape
        lat = -lat / dim_lat * self.bbox.lat_span + self.bbox.max_lat
        lng = lng / dim_lng * self.bbox.lng_span + self.bbox.min_lng

        ax = plt.axes(projection='3d')
        p = ax.plot_surface(
            lat,
            lng,
            alt,
            cmap=self.cmap,
        )
        plt.gcf().colorbar(p)

        ax.view_init(azim=22.5, elev=45)
        ax.set_xlabel('lat')
        ax.set_ylabel('lng')
        ax.set_zlabel('alt')
        ax.invert_xaxis()
