class WeatherException(Exception):
    pass


class UnknownPlaceName(WeatherException):
    pass


class ServiceNotAvailable(WeatherException):
    pass
