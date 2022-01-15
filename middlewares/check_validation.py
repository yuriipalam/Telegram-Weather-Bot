from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware

from handlers.users.start import bot_start
from loader import db


class CheckValidation(BaseMiddleware):
    async def on_process_message(self, message: types.Message, data: dict):
        current = db.check_validation(message)
        try:
            if data['raw_state'] == "Start:city":
                return
        except KeyError:
            pass
        if current is False:
            data["user_start"] = True
            try:
                if data['command'].command == "start":
                    return
            except KeyError:
                pass
            await bot_start(message)
            raise CancelHandler()
