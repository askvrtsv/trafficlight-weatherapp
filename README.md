# trafficlight-weatherapp

Тестовое задание на вакансию "Python разработчик (middle)" в Traffic Light.

## Запуск

```bash
cp weatherapp/.env-sample .env

# Перед запуском контейнеров необходимо указать в .env ключ и токен для работы с API
docker-compose up
```

Запускаются два контейнера: Django и Телеграм бот.

## Эндпоинты

### `GET http://localhost:8000/weather?city=str`

Возвращает информацию о погоде в указанном городе `city`. Названия городов, для которых можно узнать погоду, загружаются из файла `weatherapp/weather/data/places.json`

Пример возвращаемых данных:
```json
{"place":{"title":"Москва","lat":55.75,"lon":37.62},"temperature":-14.0,"wind_speed":3.6,"pressure_mm":738
```
