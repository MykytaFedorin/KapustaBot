from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_menu = ReplyKeyboardMarkup([
    [
        KeyboardButton(text="Общая информация"),
        KeyboardButton(text="Сделать заказ"),
    ]
],
    resize_keyboard=True)
