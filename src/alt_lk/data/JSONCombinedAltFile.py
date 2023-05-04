import numpy as np
from utils import Log

from alt_lk.data.JSONAltFile import JSONAltFile
from alt_lk.data.JSONBaseAltFile import JSONBaseAltFile

log = Log('JSONCombinedAltFile')

PATH = 'data/json/combined.json'


class JSONCombinedAltFile(JSONBaseAltFile):
    @property
    def path(self):
        return PATH

    def build(self):
        matrix_block = []
        for lat in range(9, 5 - 1, -1):
            matrix_row = []
            for lng in range(78, 82 + 1):
                json_alt_file = JSONAltFile((lat, lng))
                matrix = np.array(json_alt_file.read())
                matrix_row.append(matrix)
            matrix_block.append(matrix_row)
        matrix_block = np.block(matrix_block)
        return matrix_block.tolist()


if __name__ == '__main__':
    JSONCombinedAltFile().write(JSONCombinedAltFile().build())
