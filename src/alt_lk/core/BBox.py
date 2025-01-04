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

    def __str__(self) -> str:
        norm = self.norm
        return f"BBox({norm.min_latlng}, {norm.max_latlng})"

    def __hash__(self) -> int:
        return hash(self.tuple)

    @cached_property
    def min_lat(self):
        return self.min_latlng.lat

    @cached_property
    def min_lng(self):
        return self.min_latlng.lng

    @cached_property
    def max_lat(self):
        return self.max_latlng.lat

    @cached_property
    def max_lng(self):
        return self.max_latlng.lng

    @cached_property
    def lat_span(self):
        return self.max_lat - self.min_lat

    @cached_property
    def lng_span(self):
        return self.max_lng - self.min_lng

    def get_plat(self, lat: float):
        return (lat - self.min_lat) / self.lat_span

    def get_plng(self, lng: float):
        return (lng - self.min_lng) / self.lng_span

    @staticmethod
    def from_point(latlng: LatLng, span: float = 0.1):

        return BBox(
            LatLng(latlng.lat - span, latlng.lng - span),
            LatLng(latlng.lat + span, latlng.lng + span),
        )
