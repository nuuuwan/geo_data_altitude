import matplotlib.pyplot as plt
import numpy as np

from alt_lk import Alt, BBox, LatLng
from utils_future import Example


def main():
    bbox = BBox(
                LatLng(6.91966959592014, 80.75296449863315),
        LatLng(6.988336872509167, 80.82439013020513),
    )
    data = Alt.get_matrix_subset(bbox)
    arr = np.array(data)

    plt.imshow(arr, cmap='coolwarm')
    plt.colorbar()
    Example.write(__file__)


if __name__ == '__main__':
    main()
