import json
import logging
from functools import lru_cache

from cachetools import TTLCache, cached
from core.settings import BASE_DIR

from .constants import WEATHER_CACHE_SECS
from .exceptions import ServiceNotAvailable, UnknownPlaceName
from .models import Place, Weather
from .providers import YandexWeather

logger = logging.getLogger(__name__)


@lru_cache
def load_places() -> dict[str, Place]:
    places_path = BASE_DIR / "weather" / "data" / "places.json"
    with places_path.open(mode="r", encoding="utf-8") as fp:
        return {
            place["title"].lower(): Place(
                title=place["title"], lat=place["lat"], lon=place["lon"]
            )
            for place in json.load(fp)
        }


def get_place(place_name: str) -> Place:
    try:
        return load_places()[place_name.lower()]
    except KeyError:
        raise UnknownPlaceName(f'Местоположение "{place_name}" не найдено')


@cached(TTLCache(1024, WEATHER_CACHE_SECS))
def get_weather_at_place(place: Place) -> Weather:
    provider = YandexWeather()
    try:
        weather = provider.get_weather_at_place(place)
    except Exception as exp:
        logger.exception(exp)
        raise ServiceNotAvailable
    return weather
