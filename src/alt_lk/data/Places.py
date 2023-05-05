import math
import os

from utils import JSONFile, TSVFile

from alt_lk.compute._constants import LATLNG0


def get_angle(latlng0, latlng1):
    lat0, lng0 = latlng0
    lat1, lng1 = latlng1
    return 90 - math.degrees(math.atan2(lat1 - lat0, lng1 - lng0))


class Places:
    @staticmethod
    def mountains_file():
        return JSONFile(os.path.join('data', 'mountains.json'))

    @staticmethod
    def buildings_file():
        return JSONFile(os.path.join('data', 'buildings.json'))

    @staticmethod
    def mountains():
        return Places.mountains_file().read()

    @staticmethod
    def buildings():
        return Places.buildings_file().read()

    @staticmethod
    def validate_duplicates(d_list):
        latlng_set = set()
        for d in d_list:
            latlng = tuple(d['latlng'])
            if latlng in latlng_set:
                raise Exception(f'Duplicate latlng: {latlng}')
            latlng_set.add(latlng)

        name_set = set()
        for d in d_list:
            name = d['name']
            if name in name_set:
                raise Exception(f'Duplicate name: {name}')
            name_set.add(name)

    @staticmethod
    def validate(latlng0):
        for file in [Places.mountains_file(), Places.buildings_file()]:
            d_list = file.read()
            Places.validate_duplicates(d_list)
            d_list = sorted(
                d_list, key=lambda d: get_angle(latlng0, d['latlng'])
            )
            file.write(d_list)

            tsv_file_path = file.path[:-5] + '.tsv'
            TSVFile(tsv_file_path).write(d_list)


if __name__ == '__main__':
    Places.validate(LATLNG0)
