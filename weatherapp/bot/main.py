import telebot
from core.settings import TELEGRAM_TOKEN
from telebot.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

from weather import service as weather_service
from weather.exceptions import ServiceNotAvailable, UnknownPlaceName

bot = telebot.TeleBot(TELEGRAM_TOKEN, parse_mode=None)


@bot.message_handler(commands=["start"])
def start_message(message):
    keyboard = InlineKeyboardMarkup()

    button_weather = InlineKeyboardButton("Узнать погоду", callback_data="weather")
    keyboard.add(button_weather)

    bot.send_message(
        message.from_user.id, text="Привет. Что вы хотите?", reply_markup=keyboard
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call: CallbackQuery) -> None:
    if call.data == "weather":
        bot.send_message(call.message.chat.id, "В каком городе?")
        bot.register_next_step_handler(call.message, handle_weather_place)


def handle_weather_place(message: Message) -> None:
    try:
        place = weather_service.get_place(message.text)
    except UnknownPlaceName:
        bot.send_message(message.chat.id, "Не удается найти такой город")
        return None

    try:
        weather = weather_service.get_weather_at_place(place)
    except ServiceNotAvailable:
        bot.send_message(
            message.chat.id, "Сервис временно недоступен. Попробуйте позже"
        )
        return None

    bot.send_message(message.chat.id, f"{weather.temperature}°")


if __name__ == "__main__":
    bot.infinity_polling()
