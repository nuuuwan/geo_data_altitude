import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
from utils import Log

from alt_lk.alt.Alt import Alt
from alt_lk.render.AbstractPlot import AbstractPlot

log = Log("Map2D")


class Map2D(AbstractPlot):
    @property
    def cmap(self):
        # Define custom colormap
        cdict = {
            "red": [(0.0, 0.0, 0.0), (0.5, 1.0, 1.0), (1.0, 1.0, 1.0)],
            "green": [(0.0, 0.0, 0.0), (0.5, 1.0, 1.0), (1.0, 0.0, 0.0)],
            "blue": [(0.0, 1.0, 1.0), (0.5, 1.0, 1.0), (1.0, 0.0, 0.0)],
        }
        return LinearSegmentedColormap("CustomMap", cdict)

    def build_plot(self):
        log.debug("build_plot")

        if self.alt is None:
            alt = Alt.get_matrix_subset(self.bbox)
        else:
            alt = self.alt

        if self.get_mapped_alt is not None:
            alt = self.get_mapped_alt(alt)
        log.debug(f"alt.shape={alt.shape}")
        lat, lng = np.mgrid[: alt.shape[0], : alt.shape[1]]

        dim_lat, dim_lng = alt.shape
        lat = -lat / dim_lat * self.bbox.lat_span + self.bbox.max_lat
        lng = lng / dim_lng * self.bbox.lng_span + self.bbox.min_lng

        plt.scatter(
            lng,
            lat,
            c=alt,
            s=1,
            cmap=self.cmap,
            marker="s",
            vmin=-100,
            vmax=100,
        )
        plt.colorbar()

        ax = plt.gca()
        ax.set_xlabel("lng")
        ax.set_ylabel("lat")
        log.debug("build_plot done!")
