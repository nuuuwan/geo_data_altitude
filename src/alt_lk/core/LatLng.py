from dataclasses import dataclass
from functools import cached_property
import webbrowser
        

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
        norm = self.norm
        return f'LatLng({norm.lat}, {norm.lng})'

    @cached_property
    def str_formatted(self) -> str:
        return f'{self.lat:.3f}N,{self.lng:.3f}E'

    @cached_property
    def tuple(self) -> tuple[float, float]:
        return (self.lat, self.lng)

    @cached_property
    def str_03d(self) -> str:
        return f'{self.lat:03d}N.{self.lng:03d}E'

    @cached_property
    def url_google_maps(self):
        return f'https://www.google.com/maps/place/{self.str_formatted}'
    
    def open_google_maps(self):
        webbrowser.open(self.url_google_maps)