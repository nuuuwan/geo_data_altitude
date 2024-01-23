import matplotlib.pyplot as plt
import numpy as np

from alt_lk import Alt
from utils_future import Example


def main():
    data = Alt.get_alt_data_for_lk()
    arr = np.array(data)

    arr[(arr < 1)] = 0
    MAX_MAX_ALT = 10_000

    i = 1
    while True:
        min_alt = 10 ** (i / 4)
        max_alt = 10 ** ((i + 1) / 4)
        arr[(arr >= min_alt) & (arr < max_alt)] = -(i + 1)
        if max_alt > MAX_MAX_ALT:
            break
        i += 1
    plt.imshow(arr, cmap='Spectral')
    Example.write(__file__)


if __name__ == '__main__':
    main()
