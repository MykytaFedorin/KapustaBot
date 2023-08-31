from loader import dp
from loader import bot
from aiogram.types import Message
from database.db_loader import get_products
from keyboards.inline.buy_product import buy_product_kb

@dp.message_handler(commands = ['start'])
async def show_products(message: Message):
    products = await get_products()
    for product in products:
        await bot.send_photo(chat_id = message.from_id,
                             photo = product.photo, 
                             caption = product.description, 
                             reply_markup = buy_product_kb);
