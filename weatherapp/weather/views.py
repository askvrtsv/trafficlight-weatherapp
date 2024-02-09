from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from . import searializers, service
from .exceptions import ServiceNotAvailable, UnknownPlaceName


@api_view(["GET"])
def get_weather(request: Request) -> Response:
    try:
        place = service.get_place(request.GET["city"])
    except (KeyError, UnknownPlaceName):
        return Response(status=status.HTTP_404_NOT_FOUND)

    try:
        weather = service.get_weather_at_place(place)
    except ServiceNotAvailable:
        return Response(
            {"message": "Сервис временно недоступен. Попробуйте позже"},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    serializer_out = searializers.WeatherSerializer(weather)
    return Response(serializer_out.data)
