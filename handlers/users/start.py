from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import ReplyKeyboardRemove

from keyboards.default import menu
from loader import dp, db
from states import Start
from .get_weather import get_timezone


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message = None):
    text = f"Привет! Я знаю погоду во всех городах мира \U0001F601 " \
           "Для начала напиши мне город, в котором ты находишься\n\n" \
           "Если бот не находит конкретно твой город, то напиши ближайший город, где такой же часовой " \
           "пояс, как и у тебя. Это важно для синхронизации времени!"
    await message.answer(text, reply_markup=ReplyKeyboardRemove())
    await Start.city.set()


@dp.message_handler(state=Start.city)
async def bot_start_state(message: types.Message, state: FSMContext):
    timezone = await get_timezone(message)
    if timezone:
        text = 'Супер! Теперь ты будешь получать погоду своего города каждый день в 7 утра!\n\n' \
               'Также ты можешь написать название любого другого города и я скажу тебе его погоду \U0001F970'
        await message.reply(text, reply_markup=menu)
        await state.finish()
        db.add_user(user_id=message.from_user.id, user_login=message.from_user.username,
                    user_fullname=message.from_user.full_name, city=message.text, timezone=timezone)
