import os

import matplotlib.pyplot as plt
import numpy as np
from utils import Log
from utils_future import Example
from alt_lk import Alt


def main():
    data = Alt.get_alt_data_for_lk()
    arr = np.array(data)
    grad_x, grad_y = np.gradient(arr)
    slope = np.sqrt(grad_x**2 + grad_y**2)
    
    plt.imshow(slope, cmap='coolwarm')
    plt.colorbar()
    Example.write(__file__)

if __name__ == '__main__':
    main()
