from aiogram.dispatcher.filters.state import State, StatesGroup


class Orders(StatesGroup):

    GPS = State()
    contacts = State()