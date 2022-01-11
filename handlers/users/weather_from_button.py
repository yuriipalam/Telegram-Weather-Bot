from aiogram import types

from loader import dp, db
from utils.misc import rate_limit
from .get_weather import get_weather


@rate_limit(limit=60)
@dp.message_handler(text='Погода')
async def weather_from_button(message: types.Message):
    current_user = db.select_user(user_id=message.from_user.id)
    await message.reply(await get_weather(message, message_text=current_user[4]))
