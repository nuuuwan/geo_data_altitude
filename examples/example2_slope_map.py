
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import convolve

from alt_lk import Alt
from utils_future import Example


def main():
    data = Alt.get_alt_data_for_lk()
    arr = np.array(data)

    WIDTH = 1
    N = 2 * WIDTH + 1
    F2 = 1.0 * (N**2)
    kernel = np.ones((N, N)) / F2

    padded_arr = np.pad(arr, pad_width=WIDTH)
    neighborhood_avg = convolve(
        padded_arr, kernel, 
    )
    neighborhood_avg = neighborhood_avg[WIDTH:-WIDTH, WIDTH:-WIDTH]
    slope = arr - neighborhood_avg 
    
    LIMIT = 20
    slope[slope > LIMIT] = LIMIT
    slope[slope < -LIMIT] = -LIMIT


    plt.imshow(slope, cmap='bwr')
    plt.colorbar()
    Example.write(__file__)


if __name__ == '__main__':
    main()
