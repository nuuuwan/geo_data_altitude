import os
from functools import cached_property

import numpy as np
from utils import Log

log = Log('FiledNPArray')


class FiledNPArray:
    def __init__(self, key, func_get):
        self.key = key
        self.func_get = func_get

    @property
    def path(self):
        return os.path.join('data_tmp', f'{self.key}.npy')

    @cached_property
    def value(self):
        if os.path.exists(self.path):
            log.debug(f'Read {self.path}')
            return np.load(self.path)
        data = self.func_get()
        np.save(self.path, data)
        log.info(f'Wrote {self.path}')
        return data
