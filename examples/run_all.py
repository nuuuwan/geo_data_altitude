from examples import (example0, example1_lkmap_2d, example2_lkmap_3d)

EXAMPLES_LIST = [
    example0, example1_lkmap_2d, example2_lkmap_3d
]


def main():
    for example in EXAMPLES_LIST:
        example.main()


if __name__ == '__main__':
    main()
