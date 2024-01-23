
import matplotlib.pyplot as plt
import numpy as np

from alt_lk import Alt
from utils_future import Example


def main():
    data = Alt.get_alt_data_for_lk()
    arr = np.array(data)

    plt.imshow(arr, cmap='coolwarm')
    plt.colorbar()
    Example.write(__file__)


if __name__ == '__main__':
    main()
