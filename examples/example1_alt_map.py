import numpy as np
import matplotlib.pyplot as plt
from alt_lk import Alt
from utils_future import PltX


def main():
    data = Alt.matrix()
    arr = np.array(data)

    arr[arr <= 0] = -100

    plt.imshow(arr, cmap='viridis')
    plt.colorbar()

    PltX.write(__file__)


if __name__ == '__main__':
    main()
