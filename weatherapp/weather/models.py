import dataclasses


@dataclasses.dataclass(frozen=True)
class Place:
    title: str
    lat: float
    lon: float


@dataclasses.dataclass(frozen=True)
class Weather:
    place: Place
    temperature: float
    wind_speed: float
    pressure_mm: int
