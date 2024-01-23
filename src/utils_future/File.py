import os
from functools import cached_property

from utils import File as FileOld


class File(FileOld):
    def __str__(self) -> str:
        return f'{self.path} ({self.size_m:.2f}MB)'

    @cached_property
    def size(self) -> int:
        return os.path.getsize(self.path)

    @cached_property
    def size_m(self) -> float:
        return self.size / 1024 / 1024
