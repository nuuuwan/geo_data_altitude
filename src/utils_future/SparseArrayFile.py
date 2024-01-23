import numpy as np
import scipy.sparse as sp
from utils import Log

from utils_future.File import File

log = Log('SparseArrayFile')


class SparseArrayFile(File):
    def write(self, list_of_list_of_float: list[list[float]]):
        np_arr = np.array(list_of_list_of_float)
        sparray = sp.csr_matrix(np_arr)
        sp.save_npz(self.path, sparray)
        log.info(f'Wrote {self}.')

    def read(self) -> list[list[float]]:
        sparray = sp.load_npz(self.path)
        np_arr = sparray.toarray()
        list_of_list_of_float = np_arr.tolist()
        log.info(f'Read {self}.')
        return list_of_list_of_float
