import os

from utils import JSONFile, Log

log = Log('JSONAltFile')


class JSONBaseAltFile:
    @property
    def path(self):
        raise NotImplementedError

    def build(self):
        raise NotImplementedError

    def write(self, data):
        JSONFile(self.path).write(data)
        dim_x, dim_y = len(data), len(data[0])
        log.info(f'Wrote {self.path} ({dim_x} x {dim_y})')
        return data

    def read(self):
        if os.path.exists(self.path):
            return JSONFile(self.path).read()
        data = self.build()
        self.write(data)
        return data
