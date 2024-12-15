import matplotlib.pyplot as plt
import numpy as np

from alt_lk.alt.Alt import Alt
from alt_lk.render.AbstractPlot import AbstractPlot


class Map2D(AbstractPlot):
    def build_plot(self):
        alt = Alt.get_matrix_subset(self.bbox)
        lat, lng = np.mgrid[: alt.shape[0], : alt.shape[1]]

        dim_lat, dim_lng = alt.shape
        lat = -lat / dim_lat * self.bbox.lat_span + self.bbox.max_lat
        lng = lng / dim_lng * self.bbox.lng_span + self.bbox.min_lng

        alt[alt <= 0] = -0.1

        plt.scatter(lng, lat, c=alt, s=1, cmap=self.cmap, marker='s')
        plt.colorbar()

        ax = plt.gca()
        ax.set_xlabel('lng')
        ax.set_ylabel('lat')
