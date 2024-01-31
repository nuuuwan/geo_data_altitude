import os

from alt_lk.render import LKMap2D
from examples.PLACE_BBOX_IDX import PLACE_BBOX_IDX


def main():
    for place, bbox in PLACE_BBOX_IDX.items():
        place_id = place.replace(' ', '_').lower()
        image_path = os.path.join(
            'examples', 'images', f'example1_lkmap_2d.{place_id}.png'
        )
        LKMap2D(bbox).write(place, image_path)


if __name__ == '__main__':
    main()
