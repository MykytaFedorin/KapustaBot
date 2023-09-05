from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu_kb = ReplyKeyboardMarkup([
    [
        KeyboardButton(text="Показать корзину"),
        KeyboardButton(text="Показать товары"),
    ]
],
    resize_keyboard=True)
