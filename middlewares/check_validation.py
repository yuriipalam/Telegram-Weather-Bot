from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from handlers.users.start import bot_start
from loader import db


class CheckValidation(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        try:
            if data['command'].command == "start":
                return
        except KeyError:
            pass
        try:
            if data['raw_state'] is not None:
                return
        except KeyError:
            pass
        current = db.check_validation(message)
        if current is False:
            await bot_start(message)
            raise CancelHandler()
