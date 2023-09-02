from loader import dp
from loader import bot
from aiogram.types import Message, CallbackQuery
from aiogram.utils import markdown
from states import Order_
import database.db_loader as db
from keyboards.inline.buy_product import create_ikb


@dp.message_handler(commands = ['start'])
async def show_products(message: Message):
    products = await db.get_products()
    for product in products:
        markdown.bold
        description = f'{product.name} {product.price}€ \n\n{product.description}   \n\nОсталось: {product.available_amount}'
        ikb = create_ikb(f'{product.product_id}')
        await bot.send_photo(chat_id = message.from_id,
                             photo = product.photo, 
                             caption = description,
                             reply_markup = ikb)
    await Order_.pending_order.set()


@dp.message_handler(commands='make_order')
async def create_customer(message: Message):
    await db.create_customer_(telegram_id = message.from_user.id,
                             name = message.from_user.full_name, 
                             phone = '+421949175898')
    await Order_.pending_order.set()


@dp.callback_query_handler(lambda c: int(c.data) in db.get_product_ids(),
                           state=Order_.pending_order)
async def add_product_to_order(callback_query: CallbackQuery):
    product_id = callback_query.data
    product  = await db.get_product_by_id(int(product_id))
    order_id = await db.create_order(callback_query.from_user.id, product.product_id)
    await db.create_orderitem(order_id, product.product_id, product.price)
    await callback_query.answer('Товар добавлен в корзину')

