from aiogram.dispatcher.filters.state import StatesGroup, State


class AddProduct(StatesGroup):
    add_photo = State()
    add_price = State()
    add_description = State()
    add_amount = State()
    add_name = State()
