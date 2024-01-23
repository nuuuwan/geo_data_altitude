from dataclasses import dataclass
from functools import cached_property

from alt_lk.core.LatLng import LatLng


@dataclass
class BBox:
    min_latlng: LatLng
    max_latlng: LatLng

    @cached_property
    def tuple(self) -> tuple[LatLng, LatLng]:
        return (self.min_latlng, self.max_latlng)

    def __hash__(self) -> int:
        return hash(self.tuple)
