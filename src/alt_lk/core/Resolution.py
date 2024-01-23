from dataclasses import dataclass
from functools import cached_property


@dataclass
class Resolution:
    arc_seconds: int
    version: int

    def __hash__(self):
        return hash((self.arc_seconds, self.version))

    def __str__(self):
        return f'Resolution(arc_seconds={self.arc_seconds}, version={self.version})'

    @cached_property
    def dim(self) -> int:
        return 3_600 // self.arc_seconds

    @cached_property
    def dim1(self) -> int:
        return self.dim + 1

    @cached_property
    def file_code(self) -> str:
        return f'{self.arc_seconds}arc_{self.version}v'
