import os

import matplotlib.pyplot as plt
import numpy as np
from utils import Log

from alt_lk import Alt

log = Log('example1-map')


def main():
    data = Alt.get_alt_data_for_lk()
    arr = np.array(data)

    plt.imshow(arr, cmap='viridis')
    plt.colorbar()
    image_path = os.path.join('examples', 'example1-map.png')
    plt.savefig(image_path)
    log.info(f'Wrote {image_path}.')


if __name__ == '__main__':
    main()
