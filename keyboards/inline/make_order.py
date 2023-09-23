from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton



finish_order_ikb = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton(text='Оформить заказ', 
                             callback_data='finish_order'),
    ]
])
