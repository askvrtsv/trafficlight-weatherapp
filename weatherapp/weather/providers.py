import abc
import typing as t
from urllib.parse import urljoin

import requests
from core.settings import YANDEX_WEATHER_API_KEY

from .models import Place, Weather


class WeatherProvider(abc.ABC):
    @abc.abstractmethod
    def get_weather_at_place(self, place: Place) -> Weather:
        raise NotImplementedError


class YandexWeatherClient:
    def __init__(self) -> None:
        self.base_url = "https://api.weather.yandex.ru/"
        self.api_key = YANDEX_WEATHER_API_KEY

    def build_url(self, url: str) -> str:
        return urljoin(self.base_url, url.strip("/"))

    def request(
        self,
        method: str,
        url: str,
        params: dict[str, t.Any] | None = None,
    ):
        response = requests.request(
            method,
            self.build_url(url),
            params=params,
            headers={"X-Yandex-API-Key": self.api_key},
            timeout=10.0,
        )
        response.raise_for_status()
        return response.json()

    def get(self, url: str, params: dict[str, t.Any] | None = None):
        return self.request("GET", url, params=params)


class YandexWeather(WeatherProvider):
    def __init__(self) -> None:
        self.client = YandexWeatherClient()

    def get_weather_at_place(self, place: Place) -> Weather:
        params = {"lat": place.lat, "lon": place.lon}
        forecast = self.client.get("/v2/forecast", params=params)["fact"]
        return Weather(
            place=place,
            temperature=forecast["temp"],
            wind_speed=forecast["wind_speed"],
            pressure_mm=forecast["pressure_mm"],
        )
