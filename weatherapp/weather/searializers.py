from rest_framework_dataclasses.serializers import DataclassSerializer

from .models import Place, Weather


class PlaceSerializer(DataclassSerializer):
    class Meta:
        dataclass = Place


class WeatherSerializer(DataclassSerializer):
    place = PlaceSerializer()

    class Meta:
        dataclass = Weather
