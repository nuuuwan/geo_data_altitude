
from utils import Log

from alt_lk.data.GeoTIFFFile import GeoTIFFFile
from alt_lk.data.JSONBaseAltFile import JSONBaseAltFile

log = Log('JSONAltFile')


class JSONAltFile(JSONBaseAltFile):


    def __init__(self, latlng: tuple[int, int]):
        self.latlng = latlng

    @property
    def path(self):
        lat, lng = self.latlng
        return f'data/json/N{lat:03d}.E{lng:03d}.json'

    def build(self):
        tif = GeoTIFFFile(self.latlng)
        return tif.get_data()
        