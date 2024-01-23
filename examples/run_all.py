from examples import example1_map, example2_slope_map

EXAMPLES_LIST = [
    example1_map,
    example2_slope_map,
]

def main():
    for example in EXAMPLES_LIST:
        example.main()

if __name__ == '__main__':
    main()