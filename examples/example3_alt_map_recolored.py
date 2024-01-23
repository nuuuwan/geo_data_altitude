import matplotlib.pyplot as plt
import numpy as np

from alt_lk import Alt
from utils_future import Example


def main():
    data = Alt.matrix()
    arr = np.array(data)

    plt.imshow(arr, cmap='Spectral')
    Example.write(__file__)


if __name__ == '__main__':
    main()
