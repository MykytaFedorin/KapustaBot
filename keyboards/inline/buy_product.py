from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

buy_product_kb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton(text='Buy', callback_data='buy'),
    ]
])
