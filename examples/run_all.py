from examples import (example4_alt_map_colombo,
                      example5_alt_map_viharamahadevi_park,
                      example6_alt_map_nuwara_eliya)

EXAMPLES_LIST = [
    # example1_alt_map,
    # example2_slope_map,
    # example3_alt_map_recolored,
    example4_alt_map_colombo,
    example5_alt_map_viharamahadevi_park,
    example6_alt_map_nuwara_eliya,
]


def main():
    for example in EXAMPLES_LIST:
        example.main()


if __name__ == '__main__':
    main()
