import os
from functools import cached_property

import numpy as np
from utils import Log

log = Log('FiledNPArray')
DIR_DATA_TMP = 'data_tmp'


class FiledNPArray:
    def __init__(self, key, func_get):
        self.key = key
        self.func_get = func_get

    @property
    def path(self):
        if not os.path.exists(DIR_DATA_TMP):
            os.mkdir(DIR_DATA_TMP)
        return os.path.join(DIR_DATA_TMP, f'{self.key}.npy')

    @cached_property
    def value(self):
        if os.path.exists(self.path):
            log.debug(f'Read {self.path}')
            return np.load(self.path)
        data = self.func_get()
        np.save(self.path, data)
        log.info(f'Wrote {self.path}')
        return data
