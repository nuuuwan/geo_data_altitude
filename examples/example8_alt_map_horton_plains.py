import matplotlib.pyplot as plt
import numpy as np

from alt_lk import Alt, BBox, LatLng
from utils_future import Example


def main():
    bbox = BBox(
        LatLng(6.666381112559362, 80.70465850712198),
        LatLng(6.903176670504809, 80.9081260851063),
    )
    data = Alt.get_matrix_subset(bbox)
    arr = np.array(data)

    plt.imshow(arr, cmap='coolwarm')
    plt.colorbar()
    Example.write(__file__)


if __name__ == '__main__':
    main()
