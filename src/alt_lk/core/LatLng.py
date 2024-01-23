from dataclasses import dataclass
from functools import cached_property


@dataclass
class LatLng:
    lat: float
    lng: float

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, LatLng):
            return False
        return self.tuple == o.tuple

    def __hash__(self) -> int:
        return hash(self.tuple)

    def __str__(self) -> str:
        return f'{self.lat:.4f}°N, {self.lng:.4f}°E'

    @cached_property
    def tuple(self) -> tuple[float, float]:
        return (self.lat, self.lng)

    @cached_property
    def str_03d(self) -> str:
        return f'{self.lat:03d}N.{self.lng:03d}E'
