from aiogram.dispatcher.filters.state import State, StatesGroup


class Search(StatesGroup):
    first_lvl = State()
    second_lvl = State()
