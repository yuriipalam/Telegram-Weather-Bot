import datetime
import random

import requests
from aiogram import types
from suntime import Sun

from data.config import WEATHER_TOKENS, SERVER_TIMEZONE
from .additionals import Orphography, weather_smiles, monthes


async def get_weather(message: types.Message = None, message_text: str = None, message_fullname: str = None):
    if not message_text:
        message_text = message.text
    if not message_fullname:
        message_fullname = message.from_user.full_name

    token = random.choice(WEATHER_TOKENS)

    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={message_text}&lang=ru&units=metric&appid={token}")

    data = response.json()

    if data['cod'] == '404':
        await message.reply("Город не найден")
        return False

    city_real_name = data['name']  # название города
    temp = data['main']['temp']  # температура градусы цельсия
    feels_temp = data['main']['feels_like']  # ощущается градусы цельсия
    humidity = data['main']['humidity']  # влажность %
    # pressure = data['main']['pressure']  # давление мм.рт.ст
    wind = data['wind']['speed']  # ветер м/c
    description = data['weather'][0]['description'].capitalize()  # описание погоды

    # рассвет, закат, длительность светового дня
    timezone = data['timezone'] // 3600  # узнаем таймзон

    coord_lat = data['coord']['lat']  # координаты лат
    coord_lon = data['coord']['lon']  # координаты лон

    sun = Sun(coord_lat, coord_lon)  # узнаем данные о положении солнца по координатам благодаря библиотеке

    hashed_sunrise = sun.get_sunrise_time()  # восход, для дальнейшей обработки
    hashed_sunset = sun.get_sunset_time()  # закат, для дальнейшей обработки

    real_sunrise_hours = hashed_sunrise.hour + timezone
    real_sunset_hours = hashed_sunset.hour + timezone

    # обработка данных восхода и заката
    if real_sunrise_hours >= 24:
        real_sunrise_hours -= 24
    if real_sunset_hours >= 24:
        real_sunset_hours -= 24

    if timezone < 0:
        if hashed_sunrise.hour < timezone * (-1):
            real_sunrise_hours = timezone + hashed_sunrise.hour + 24
        if hashed_sunset.hour < timezone * (-1):
            real_sunset_hours = timezone + hashed_sunset.hour + 24

    real_sunrise = datetime.datetime(hashed_sunrise.year, hashed_sunrise.month, hashed_sunrise.day,
                                     real_sunrise_hours,
                                     hashed_sunrise.minute)
    real_sunset = datetime.datetime(hashed_sunset.year, hashed_sunset.month, hashed_sunset.day,
                                    real_sunset_hours,
                                    hashed_sunset.minute)

    # точное время запроса и его обработка
    time_date = datetime.datetime.now()
    if timezone < 0:
        timezone *= -1
        time_date -= datetime.timedelta(hours=SERVER_TIMEZONE + timezone)
    else:
        time_date -= datetime.timedelta(hours=SERVER_TIMEZONE - timezone)

    # массив часы:минуты:секунды - длителность светого дня
    delta_day_length = str((real_sunset - real_sunrise)).split(":")

    # эмоджи рядом с описание погоды
    icon_smile_id = data['weather'][0]['icon']

    # описание с эмоджи
    description_with_emoji = f"{description} {weather_smiles[icon_smile_id]}"

    # длительность светового дня
    if delta_day_length[1] == '00':
        sun_length = f"Длительность светового дня: {delta_day_length[0]} часов"
    else:
        sun_length = f"Длительность светового дня: {delta_day_length[0]} часов и " \
                     f"{Orphography.end_of_numbers(delta_day_length[1])} " \
                     f"минут{Orphography.end_of_words(int(delta_day_length[1]))}"

    # вывод температуры, и того как она ощущается
    if temp > feels_temp + 2.5 or temp < feels_temp - 2.5:
        temp = f"Температура: {round(temp, 1)}°C, ощущается как {round(feels_temp, 1)}°C"
    else:
        temp = f"Температура: {round(temp, 1)}°C"

    current_time = f"{time_date.day} {monthes[time_date.month]}, {time_date.strftime('%H:%M')}"

    return (f"*** {current_time} ***\n\n"
            f"{city_real_name}, {description_with_emoji}\n\n"
            f"{temp}\n"
            f"Влажность: {humidity}%\n"
            f"Ветер: {wind} м/с\n\n"
            f"Восход в {real_sunrise.strftime('%H:%M')}\n"
            f"Закат в {real_sunset.strftime('%H:%M')}\n"
            f"{sun_length}\n\n"
            f"*** Хорошего дня, {message_fullname}! ***")


async def get_timezone(message: types.Message):
    token = random.choice(WEATHER_TOKENS)

    response = requests.get(
        f"https://api.openweathermap.org/data/2.5/weather?q={message.text}&lang=ru&units=metric&appid={token}")

    data = response.json()

    if data['cod'] == '404':
        await message.reply("Город не найден")
        return False

    timezone = data['timezone'] // 3600

    return timezone
