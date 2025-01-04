import os

# import numpy as np
from scipy.ndimage import uniform_filter
from utils import Log

from alt_lk import BBox, LatLng, Map2D
from examples.PLACE_BBOX_IDX import PLACE_BBOX_IDX

log = Log("example5_derivative")


def main():

    dir_group = os.path.join("examples", "images", "example5_derivative")
    os.makedirs(dir_group, exist_ok=True)

    place_name = "Sri Lanka"
    bbox = BBox(LatLng(5.9, 79.5), LatLng(9.9, 81.9))

    # place_name = "Nuwara Eliya"
    # bbox = PLACE_BBOX_IDX[place_name]

    SIZE = 10
    log.debug(f"{place_name=}")
    log.debug(f"{SIZE=}")
    image_path = os.path.join(dir_group, f"{place_name}-{SIZE}.png")

    def get_mapped_alt(alt):
        d = alt - uniform_filter(alt, size=SIZE, mode="constant", cval=0)

        return d[SIZE:-SIZE, SIZE:-SIZE]

    Map2D(
        bbox=bbox,
        get_mapped_alt=get_mapped_alt,
    ).write(place_name, image_path, force=True)


if __name__ == "__main__":
    main()
