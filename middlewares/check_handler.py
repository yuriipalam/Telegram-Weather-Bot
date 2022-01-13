import emoji
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from string import punctuation

punctuation = [x for x in punctuation]


class CheckHandler(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        def dirty_text_checker(text):
            if text == "/start":
                return False
            for i in text:
                if i in punctuation:
                    return True
            if emoji.emoji_count(text) > 0:
                return True
            if len(text) > 30:
                return True
            if len(text) == 1:
                return True

        if dirty_text_checker(message.text):
            await message.reply("Вводи корректное название города \U0001F92C")
            raise CancelHandler()
