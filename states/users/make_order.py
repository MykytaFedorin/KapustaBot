from aiogram.dispatcher.filters.state import StatesGroup, State


class Order_(StatesGroup):
    start_order = State()
    pending_order = State()
    end_order = State()
