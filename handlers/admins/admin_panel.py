from aiogram import types

from filters import IsAdmin
from loader import dp, db


@dp.message_handler(IsAdmin(), text="/ahelp")
async def admin_help(message: types.Message):
    await message.reply("Команды для админа:\n\n"
                        "/load_log - выгрузить лог бота\n"
                        "/load_auto_sender_log - выгрузить лог автоматической рассылки погоды\n"
                        "/load_db - выгрузить базу данных")


@dp.message_handler(IsAdmin(), text="/load_log")
async def log_send(message: types.Message):
    with open(rf"log.txt", 'rb') as file:
        await message.reply_document(file)


@dp.message_handler(IsAdmin(), text="/load_auto_sender_log")
async def log_send(message: types.Message):
    with open(rf"auto_sender_log.txt", 'rb') as file:
        await message.reply_document(file)


@dp.message_handler(IsAdmin(), text="/load_db")
async def db_send(message: types.Message):
    current_db = db.select_all_users()
    amount_of_users = len(current_db)
    output_string = "*** База Данных ***\n\n" \
                    "ID | ID_telegram, Имя Логин | Город UTC | Подписка\n\n\n"
    for i in current_db:
        sub_status = ""
        if i[6] == 1:
            sub_status = "Подписка включена"
        if i[6] == 0:
            sub_status = "Подписка отключена"

        timezone = int()
        if i[5] > 0:
            timezone = f"+{i[5]}"
        if i[5] <= 0:
            timezone = i[5]

        output_string += f"{i[0]} | {i[1]}, {i[2]} {i[3]} | {i[4]}  {timezone} | {sub_status}\n\n"

    output_string += f"\nВсего {amount_of_users} пользователей"
    await message.answer(output_string)
