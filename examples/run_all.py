from examples import (example1_alt_map, example2_slope_map,
                      example3_alt_map_recolored)

EXAMPLES_LIST = [
    example1_alt_map,
    example2_slope_map,
    example3_alt_map_recolored,
]


def main():
    for example in EXAMPLES_LIST:
        example.main()


if __name__ == '__main__':
    main()
