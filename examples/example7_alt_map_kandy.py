import matplotlib.pyplot as plt
import numpy as np

from alt_lk import Alt, BBox, LatLng
from utils_future import Example


def main():
    bbox = BBox(
        LatLng(7.263741575093108, 80.58389833079025),
        LatLng(7.332285244984741, 80.67434703330403),
    )
    data = Alt.get_matrix_subset(bbox)
    arr = np.array(data)

    plt.imshow(arr, cmap='coolwarm')
    plt.colorbar()
    Example.write(__file__)


if __name__ == '__main__':
    main()
