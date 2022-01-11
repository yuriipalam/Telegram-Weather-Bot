from aiogram.dispatcher.filters.state import StatesGroup, State


class Start(StatesGroup):
    city = State()


class ChangeCity(StatesGroup):
    city = State()
