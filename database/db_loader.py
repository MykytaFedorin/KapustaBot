import psycopg2 as psql
from decimal import Decimal
from psycopg2.errors import UniqueViolation
from typing import NamedTuple
from aiogram.types import InputFile
from data import data_dir_path
from data.config import db_user, db_database
from decimal import Decimal
from datetime import datetime
from typing import List


connection = psql.connect(f"dbname={db_database} user={db_user}")
cursor = connection.cursor()

class Product(NamedTuple):
    product_id: int
    name: str
    description: str
    price: Decimal
    photo: InputFile
    available_amount: int


class Orderitem(NamedTuple):
    item_id: int
    order_id: int
    product_id: int
    quantity: int
    subtotal: Decimal


async def finish_order(order_id:int) -> None:
    ''' Switch order with provided id in FINISH status'''
    cursor.execute(f'''UPDATE order_ SET status = 'FINISH' WHERE order_id = {order_id}''')
    connection.commit()


async def update_total(order_id: int) -> None:
    '''Updates total price of an order'''
    total_price = await get_order_total(order_id)
    cursor.execute(f'''UPDATE order_ SET total_price = {total_price} WHERE order_id = {order_id}''')
    connection.commit()


async def get_order_total(order_id: int) -> Decimal:
    cursor.execute(f'''SELECT subtotal FROM orderitem WHERE order_id = {order_id}''')
    prices = cursor.fetchall()
    total = Decimal(0)
    for price in prices:
        total += price[0]
    return total


async def get_orderitems(order_id) -> list[Orderitem]:
    '''Return the list of orderitems which belongs to order with provided id'''
    cursor.execute(f'''SELECT * FROM orderitem WHERE order_id = {order_id}''')
    items = cursor.fetchall()
    res_items = list()
    for item in items:
        res_items.append(Orderitem(item_id = item[0],
                                   order_id = item[1],
                                   product_id = item[2],
                                   quantity = item[3],
                                   subtotal = item[4]))
    return res_items


async def create_customer_(telegram_id: int, name: str):
    '''Create a record with customer info'''
    try:
        cursor.execute(f'''INSERT INTO customer 
                          (telegram_id, name)
                          VALUES ({telegram_id}, '{name}');''');
    except UniqueViolation as ex:
        pass
    connection.commit()


async def get_products() -> list[Product]:
    '''return all products available to buy
       in the form of Product objects'''
    products_wrapped = list()
    cursor.execute('''SELECT * FROM product;''')
    products_raw = cursor.fetchall()
    for product in products_raw:
        photo_path = data_dir_path + product[4]
        products_wrapped.append(Product(product_id = product[0],
                                        name = product[1],
                                        description = product[2],
                                        price = product[3], 
                                        photo = InputFile(photo_path), 
                                        available_amount = product[5]))
    return products_wrapped 


async def get_cart_text(order_id: int) -> str:
    '''return a string with full
    description of which products are now in cart''' 
    items = await get_orderitems(order_id)
    cart_text = 'Корзина: \n\n'
    for index, item in enumerate(items):
        product = await get_product_by_id(item.product_id)
        cart_text += f'{index+1}. {product.name} {item.quantity}шт. {product.price}€\n\n'
    total = await get_order_total(order_id)
    cart_text += f'Всего: {total}€'
    return cart_text


def get_product_ids() -> list[int]:
    '''return a list of all product id's'''
    cursor.execute('''SELECT product_id FROM product;''')
    return [int(id_[0]) for id_ in cursor.fetchall()]


async def create_order(customer_id: int) -> int:
    '''intiales the order in db'''
    while True:
        try:
            cursor.execute(f'''SELECT order_id FROM order_ 
                              WHERE customer_id = {customer_id} AND status = 'PENDING'; ''')
            id_ = cursor.fetchall()[0][0]
            break
        except IndexError:
            cursor.execute(f'''INSERT INTO order_ 
                              (customer_id, total_price, status)
                              VALUES 
                              ({customer_id}, 0.00, 'PENDING');''')
            connection.commit()
    return id_


async def create_customer(customer_id: int, name: str, phone: str):
    '''creates customer in db'''
    cursor.execute(f'''INSERT INTO customer 
                      (customer_id, name, phone)
                      VALUES 
                      ({customer_id}, '{name}', '{phone}');''')
    connection.commit()


async def create_orderitem(order_id: int, product_id: int, price: Decimal):
    '''creates an orderitem record in db'''
    cursor.execute(f'''SELECT quantity FROM orderitem WHERE
                      order_id = {order_id} AND product_id = {product_id};''')
    quantity = cursor.fetchone()
    if quantity is None:
        cursor.execute(f'''INSERT INTO orderitem 
                          (order_id, product_id, quantity, subtotal)
                          VALUES
                          ({order_id}, {product_id}, 1, {price:.2f})''');
    else:
        cursor.execute(f'''UPDATE orderitem SET 
                           quantity = {quantity[0]+1},
                           subtotal = {(quantity[0]+1)*price:.2f}
                           WHERE product_id = {product_id};''')
    connection.commit()


async def get_product_by_id(product_id: int) -> Product:
    '''return Product object with provided id'''
    cursor.execute(f'''SELECT * FROM product WHERE product_id = {product_id};''') 
    product = cursor.fetchall()[0]
    photo_path = data_dir_path + product[4]
    return Product(product_id = product[0],
                   name = product[1],
                   description = product[2],
                   price = product[3], 
                   photo = InputFile(photo_path), 
                   available_amount = product[5])


async def create_product(name: str, description: str, 
                         price: Decimal, image_url: str, amount: int):
    '''Creates new product record in db'''
    cursor.execute(f'''INSERT INTO product 
                    (name, description, price, image_url, amount)
                    VALUES
                    ('{name}', '{description}', {price}, '{image_url}', {amount})''')
    connection.commit()


async def get_customer_ids() -> List[int]:
    '''Return all customers ids'''
    cursor.execute(f'''SELECT telegram_id FROM customer''')
    values = cursor.fetchall()
    ids = [int(value[0]) for value in values]
    return ids
