from dataclasses import dataclass


@dataclass
class LatLng:
    lat: float
    lng: float

    def __str__(self) -> str:
        return f'{self.lat}N.{self.lng})E'
