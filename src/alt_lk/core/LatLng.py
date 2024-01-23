from dataclasses import dataclass
from functools import cached_property


@dataclass
class LatLng:
    lat: float
    lng: float

    @cached_property
    def tuple(self) -> tuple[float, float]:
        return (self.lat, self.lng)

    def __str__(self) -> str:
        return f'{self.lat:.6f}°N, {self.lng:.6f}°E'

    @cached_property
    def str_03d(self) -> str:
        return f'{self.lat:03d}N.{self.lng:03d}E'

    def __hash__(self) -> int:
        return hash(self.tuple)
