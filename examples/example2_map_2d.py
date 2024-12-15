import os

from alt_lk.render import Map2D
from examples.PLACE_BBOX_IDX import PLACE_BBOX_IDX


def main():
    for place, bbox in PLACE_BBOX_IDX.items():
        place_id = place.replace(' ', '_').lower()
        dir_group = os.path.join(
            'examples', 'images', 'example2_map_2d'
        )
        os.makedirs(dir_group, exist_ok=True)
        image_path = os.path.join(
            dir_group, f'{place_id}.png'
        )
        Map2D(bbox).write(place, image_path)


if __name__ == '__main__':
    main()
