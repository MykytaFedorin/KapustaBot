from aiogram.dispatcher.filters.state import StatesGroup, State


class ProductSettings(StatesGroup):
    set_photo = State()
    set_price = State()
    set_description = State()
    set_name = State()
