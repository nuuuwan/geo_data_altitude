import math
import webbrowser
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
        return self.str_formatted

    @cached_property
    def str_formatted(self) -> str:
        return f"{self.lat:.6f},{self.lng:.6f}"

    @cached_property
    def tuple(self) -> tuple[float, float]:
        return (self.lat, self.lng)

    @cached_property
    def str_03d(self) -> str:
        return f"{self.lat:03d}N.{self.lng:03d}E"

    @cached_property
    def url_google_maps(self):
        return f"https://www.google.com/maps/place/{self.str_formatted}"

    def open_google_maps(self):
        webbrowser.open(self.url_google_maps)

    def distance(self, other):
        # compute distance in KM from first principles
        lat1 = math.radians(self.lat)
        lng1 = math.radians(self.lng)
        lat2 = math.radians(other.lat)
        lng2 = math.radians(other.lng)
        dlat = lat2 - lat1
        dlng = lng2 - lng1
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2) ** 2
        )
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        return 6371 * c
