import matplotlib.pyplot as plt
import numpy as np

from alt_lk import Alt, BBox, LatLng
from utils_future import Example


def main():
    bbox = BBox(
        LatLng(6.912032282921783, 79.85572282625117),
        LatLng(6.916671622967184, 79.86473551211941),
    )
    data = Alt.get_matrix_subset(bbox)
    arr = np.array(data)

    plt.imshow(arr, cmap='coolwarm')
    plt.colorbar()
    Example.write(__file__)


if __name__ == '__main__':
    main()
