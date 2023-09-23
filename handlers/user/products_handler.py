from loader import dp
from aiogram.dispatcher import FSMContext
from loader import bot
from aiogram.types import Message, CallbackQuery, ParseMode
from aiogram.utils import markdown
from data import admins_id
from states import Order_
import database.db_loader as db
from keyboards.inline.buy_product import create_ikb
from keyboards.inline import finish_order_ikb
from keyboards.default_keyboards import menu_kb


@dp.message_handler(commands = 'start', state='*')
async def start(message: Message, state: FSMContext):
    text = '''Привет 😃, рады видеть Вас в нашей лавке 🥳.\nДавайте я покажу вам сколько у нас есть всего вкусного 🤤.'''
    await message.answer(text=text, 
                         reply_markup=menu_kb)
    await show_products(message, state)


@dp.message_handler(text = 'Показать товары',
                    state = '*')
async def show_products(message: Message, state: FSMContext):
    await db.create_customer_(telegram_id = message.from_user.id,
                             name = message.from_user.full_name)
    order_id = await db.create_order(message.from_user.id)
    await state.update_data(order_id=order_id)
    await state.update_data(customer_name=message.from_user.full_name)
    products = await db.get_products()
    for product in products:
        description = f'{product.name} {product.price}€ \n\n{product.description}   \n\nОсталось: {product.available_amount}'
        ikb = create_ikb(f'{product.product_id}')
        await bot.send_photo(chat_id = message.from_id,
                             photo = product.photo, 
                             caption = description,
                             reply_markup = ikb,
                             parse_mode=ParseMode.HTML)
    await Order_.pending_order.set()


@dp.message_handler(text = 'Показать корзину', state = '*')
async def show_cart(message: Message, state: FSMContext):
    state_data = await state.get_data()
    try:
        order_id = state_data['order_id']
        cart_text = await db.get_cart_text(order_id)
        await message.answer(text=cart_text,
                             reply_markup=finish_order_ikb)
        await Order_.cart_watching.set()
    except KeyError:    
        await message.answer(text="Корзина пуста")
    

@dp.callback_query_handler(lambda c: c.data == 'finish_order', 
                           state = Order_.cart_watching)
async def finish_order(callback_query: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    order_id = state_data['order_id']
    customer_name = state_data['customer_name']
    order_text = await db.get_cart_text(order_id)
    order_text = order_text.replace('Корзина:', f'Заказ №{order_id} {customer_name}')
    await Order_.end_order.set()
    await db.finish_order(order_id)
    for id_ in admins_id:
        await bot.send_message(chat_id=id_,
                               text=order_text)
    await bot.send_message(chat_id=callback_query.from_user.id, text=order_text)


@dp.callback_query_handler(lambda c: int(c.data) in db.get_product_ids(),
                           state='*')
async def add_product_to_order(callback_query: CallbackQuery, state: FSMContext):
    product_id = callback_query.data
    product  = await db.get_product_by_id(int(product_id))
    data = await state.get_data()
    order_id = data['order_id']
    await db.create_orderitem(order_id, product.product_id, product.price)
    await db.update_total(order_id)
    await callback_query.answer('Товар добавлен в корзину')

