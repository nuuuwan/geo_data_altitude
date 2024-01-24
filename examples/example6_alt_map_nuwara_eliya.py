import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

from alt_lk import Alt, BBox, LatLng
from utils_future import Example


def main():
    bbox = BBox(
        LatLng(6.902851424723703, 80.58878931660789),  # Hatton
        LatLng(7.112105098302233, 80.92204999330954),  # Thiripaha
    )
    data = Alt.get_matrix_subset(bbox)
    arr = np.array(data)

    colors = ["darkgreen", "green", "yellow", "orange", "red", "brown"]
    cmap = mcolors.LinearSegmentedColormap.from_list('custom', colors)

    plt.imshow(arr, cmap=cmap)
    Example.write(__file__)


if __name__ == '__main__':
    main()
