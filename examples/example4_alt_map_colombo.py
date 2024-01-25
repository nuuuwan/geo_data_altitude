import matplotlib.pyplot as plt
import numpy as np

from alt_lk import Alt, BBox, LatLng
from utils_future import Example


def main():
    bbox = BBox(
        LatLng(6.880078017904935, 79.82096863616397),
        LatLng(6.958174410944311, 79.94629291844821),
    )
    data = Alt.get_matrix_subset(bbox)
    arr = np.array(data)

    Example.write(arr, __file__)


if __name__ == '__main__':
    main()
