import asyncio
import codecs
import datetime

import emoji

from data.config import SERVER_TIMEZONE
from loader import bot, db
from .get_weather import get_weather


async def weather_auto_sender():
    while True:
        all_users = db.select_all_users()

        for i in all_users:
            time_date = datetime.datetime.now()
            if i[6] == 1:
                user_timezone = i[5]
                if i[6] < 0:
                    user_timezone *= -1
                    time_date -= datetime.timedelta(hours=SERVER_TIMEZONE + user_timezone)
                else:
                    time_date -= datetime.timedelta(hours=SERVER_TIMEZONE - user_timezone)
                if time_date.hour == 7:
                    current_weather = await get_weather(message_text=i[4], message_fullname=i[2])
                    await bot.send_message(i[1], current_weather)
                    with codecs.open("auto_sender_log.txt", 'a', encoding="windows-1251") as file:
                        text = f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {i[2]} {i[3]} {i[4]}\n"
                        file.write(emoji.demojize(text, delimiters=(":", ":")))
        time_date = datetime.datetime.now()
        time_delta = [60 - time_date.minute, 60 - time_date.second]
        await asyncio.sleep(time_delta[0] * 60 + time_delta[1] - 60)
