from loader import dp, bot
from aiogram.types import Message, ContentType
from data import admins_id, data_dir_path 
from database import db_loader as db
from aiogram.dispatcher import FSMContext
from states import AddProduct


@dp.message_handler(lambda message: message.from_user.id in admins_id,
                    commands='my_products', 
                    state="*")
async def show_products(message: Message):
    '''Show all existing products to admin'''
    products = await db.get_products()
    for product in products:
        description = f'{product.name} {product.price}€ \n\n{product.description}   \n\nОсталось: {product.available_amount}'
        await bot.send_photo(chat_id = message.from_id,
                             photo = product.photo, 
                             caption = description)


@dp.message_handler(commands='share_message',
                    state='*')
async def share_message(message: Message):
    text = message.text.replace("/share_message", "")
    ids = await db.get_customer_ids()
    for id_ in ids:    
        await bot.send_message(chat_id=id_, text = text)


@dp.message_handler(lambda message: message.from_user.id in admins_id,
                    commands='add_product',
                    state='*')
async def start_add_product(message: Message):
    await message.answer('Как будет называться продукт?')
    await AddProduct.add_name.set() 


@dp.message_handler(lambda message: message.from_user.id in admins_id,
                    state=AddProduct.add_name)
async def add_name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await message.answer(f'Сколько будет стоить {name}?')
    await AddProduct.add_price.set()


@dp.message_handler(lambda message: message.from_user.id in admins_id,
                    state=AddProduct.add_price)
async def add_price(message: Message, state: FSMContext):
    price = message.text
    await state.update_data(price=price)
    await message.answer('Опишите товар.')
    await AddProduct.add_description.set()



@dp.message_handler(lambda message: message.from_user.id in admins_id,
                    state=AddProduct.add_description)
async def add_description(message: Message, state: FSMContext):
    description = message.text
    await state.update_data(description=description)
    await message.answer('Какое кол-во товара у вас есть?')
    await AddProduct.add_amount.set()


@dp.message_handler(lambda message: message.from_user.id in admins_id,
                    state=AddProduct.add_amount)
async def add_amount(message: Message, state: FSMContext):
    amount = message.text
    await state.update_data(amount=amount)
    await message.answer('Пришлите фото товара')
    await AddProduct.add_photo.set()

@dp.message_handler(content_types = ContentType.PHOTO,
                    state=AddProduct.add_photo)
async def add_photo(message: Message, state: FSMContext):
    photo = message.photo[-1]

    # Get file information for the photo
    file_info = await bot.get_file(photo.file_id)
    file_path = file_info.file_path
    data = await state.get_data()
    product_name = data.get('name')
    image_url = f'images/{product_name}.jpg'
    await bot.download_file(file_path, 
                            destination=f'{data_dir_path}{image_url}')
    await db.create_product(name=product_name,
                            description=data.get('description'),
                            price=data.get('price'),
                            image_url=image_url,
                            amount = data.get('amount'))
    await message.answer('Товар добавлен в каталог')
    await state.finish()
