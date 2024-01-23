import matplotlib.pyplot as plt
import numpy as np

from alt_lk import Alt, BBox, LatLng
from utils_future import Example


def main():
    bbox = BBox(
        LatLng(6.877592362039065, 79.80586994740908),
        LatLng(6.969004887718514, 79.92979946615739),
    )
    data = Alt.get_matrix_subset(bbox)
    arr = np.array(data)

    plt.imshow(arr, cmap='coolwarm')
    plt.colorbar()
    Example.write(__file__)


if __name__ == '__main__':
    main()
