from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton('Погода'),
            KeyboardButton('Помощь')
        ]
    ],
    resize_keyboard=True
)
