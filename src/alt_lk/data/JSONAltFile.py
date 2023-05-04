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
    
    def buildAndWrite(self):
        tif = GeoTIFFFile(self.latlng)
        data = tif.get_data()
        if data is None:
            log.error(f'Failed to read {self.path}')
            return None
        JSONFile(self.path).write(data)
        dim_x, dim_y = len(data), len(data[0])
        log.info(f'Wrote {self.path} ({dim_x} x {dim_y})')
        return data

    def read(self):
        if os.path.exists(self.path):
            return JSONFile(self.path).read()
        data = self.buildAndWrite()
        return data


