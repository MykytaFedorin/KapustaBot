from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def create_ikb(callback_data: str) -> InlineKeyboardMarkup:
    buy_product_kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
        [
            InlineKeyboardButton(text="🛍 Добавить в корзину 🛍", 
                                 callback_data=callback_data),
        ]
    ])
    return buy_product_kb
