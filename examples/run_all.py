from examples import example1, example2_map_2d, example3_map_3d

EXAMPLES_LIST = [example1, example2_map_2d, example3_map_3d]


def main():
    for example in EXAMPLES_LIST:
        example.main()


if __name__ == '__main__':
    main()
