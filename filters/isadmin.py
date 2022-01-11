from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data.config import admins


class IsAdmin(BoundFilter):
    async def check(self, update: types.Message):
        return update.from_user.id in admins
