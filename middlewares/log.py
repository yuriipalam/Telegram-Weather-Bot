from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
import codecs
import emoji
from datetime import datetime


class HandlersLogger(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        with codecs.open("log.txt", 'a', encoding="windows-1251") as file:
            text = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} @{message.from_user.username} " \
            f"{message.from_user.full_name}: {message.text}\n"
            file.write(emoji.demojize(text, delimiters=(":", ":")))
