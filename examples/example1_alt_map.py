import numpy as np

from alt_lk import Alt
from utils_future import Example



def main():
    data = Alt.matrix()
    arr = np.array(data)

    arr[arr <= 0] = -100

    Example.write(arr, __file__)


if __name__ == '__main__':
    main()
