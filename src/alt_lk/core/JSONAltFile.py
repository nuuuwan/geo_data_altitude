import os

from utils import JSONFile, Log

from alt_lk.core.GeoTIFFFile import GeoTIFFFile

log = Log('JSONAltFile')


class JSONAltFile:
    def __init__(self, latlng: tuple[int, int]):
        self.latlng = latlng

    @property
    def path(self):
        lat, lng = self.latlng
        return f'data/json/N{lat:03d}.E{lng:03d}.json'

    def read(self):
        if os.path.exists(self.path):
            log.warning(f'{self.path} exists')
        tif = GeoTIFFFile(self.latlng)
        data = tif.get_data()
        if data is None:
            log.error(f'Failed to read {self.path}')
            return None
        JSONFile(self.path).write(data)
        dim_x, dim_y = len(data), len(data[0])
        log.info(f'Wrote {self.path} ({dim_x} x {dim_y})')

    @staticmethod
    def combine(json_alt_file_list: list):
        data = []
        for json_alt_file in json_alt_file_list:
            data_item = json_alt_file.read()
            if data_item:
                data.extend(data_item)

        combined_path = 'data/json/all.json'
        JSONFile(combined_path).write(data)


if __name__ == '__main__':
    json_file_list = []
    for lat in [5, 6, 7, 8, 9]:
        for lng in [78, 79, 80, 81]:
            json_file = JSONAltFile((lat, lng))
            json_file_list.append(json_file)
    JSONAltFile.combine(json_file_list)
