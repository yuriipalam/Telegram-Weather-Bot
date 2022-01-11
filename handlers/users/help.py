from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from .get_weather import get_timezone
from keyboards.inline.help_menu import help_buttons_on_sub, help_buttons_off_sub
from loader import dp, bot, db
from states.main_states import ChangeCity


@dp.message_handler(Text(equals=['/help', 'Помощь']))
async def bot_help(message: types.Message, middleware_data=True):
    if middleware_data is False:
        return
    current_user = db.select_user(user_id=message.from_user.id)
    if current_user[6] == 1:
        help_buttons = help_buttons_off_sub
    else:
        help_buttons = help_buttons_on_sub
    await message.reply(
        "Я могу тебе сказать погоду любого города мира! (ну почти) \U0001F643 Для этого просто напиши мне "
        "название нужного города\n\nЕсли ты хочешь изменить свой основной город или отказаться от утренней "
        "рассылки погоды, то нажми на соответствующую кнопку ниже", reply_markup=help_buttons)


@dp.callback_query_handler(text="change_city")
async def change_city_callback(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id)
    await call.message.delete()
    await bot.send_message(call.from_user.id,
                           "Напиши мне название своего нового города \U0001F60E\n\n"
                           "Если бот не находит конкретно твой город, "
                           "то напиши ближайший город, где такой же часовой "
                           "пояс, как и у тебя. Это важно для синхронизации времени!")
    await ChangeCity.city.set()


@dp.message_handler(state=ChangeCity.city)
async def process_change_city_callback(message: types.Message, state: FSMContext):
    timezone = await get_timezone(message)
    current_user = db.select_user(user_id=message.from_user.id)
    if timezone:
        if current_user[4] == message.text:
            await state.finish()
            return await message.reply(
                "У тебя и так установлен этот город \U0001F926 Процесс смены города останавливаю...")
        await message.reply("Супер! Теперь у тебя новый город \U0001F9D0")
        db.change_city((message.text, timezone, message.from_user.id))
    await state.finish()


@dp.callback_query_handler(text="off_sub")
async def change_city_callback(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id)
    current_user = db.select_user(user_id=call.from_user.id)
    await call.message.delete()
    if current_user[6] == 1:
        db.change_subscription((False, call.from_user.id))
        await bot.send_message(call.from_user.id, "Подписка отключена \U0001F614\U0001F446")
    else:
        await bot.send_message(call.from_user.id, "Подписка и так отключена \U0001F614\U0001F446")


@dp.callback_query_handler(text="on_sub")
async def change_city_callback(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id)
    current_user = db.select_user(user_id=call.from_user.id)
    await call.message.delete()
    if current_user[6] == 0:
        db.change_subscription((True, call.from_user.id))
        await bot.send_message(call.from_user.id, "Подписка включена \U0001F60E")
    else:
        await bot.send_message(call.from_user.id, "Подписка уже включена \U0001F60E")


@dp.callback_query_handler(text="close_menu")
async def callback_close(call: types.CallbackQuery):
    await bot.answer_callback_query(call.id)
    await call.message.delete()
