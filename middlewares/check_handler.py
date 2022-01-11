import emoji
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware


class CheckHandler(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        if emoji.emoji_count(message.text) > 0 or len(message.text) > 30 or len(message.text) == 1:
            await message.reply("Вводи корректное название города \U0001F92C")
            raise CancelHandler()
