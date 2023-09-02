import psycopg2 as psql
from psycopg2.errors import UniqueViolation
from typing import NamedTuple
from aiogram.types import InputFile
from data import data_dir_path
from datetime import datetime


connection = psql.connect("dbname=myshop user=nikita")
cursor = connection.cursor()

class Product(NamedTuple):
    product_id: int
    name: str
    description: str
    price: float
    photo: InputFile
    available_amount: int

async def create_customer_(telegram_id: int, name: str, phone: str):
    '''Create a record with customer info'''
    try:
        cursor.execute(f'''INSERT INTO customer 
                          (telegram_id, name, phone)
                          VALUES ({telegram_id}, '{name}', '{phone}');''');
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
def get_product_ids() -> list[int]:
    '''return a list of all product id's'''
    cursor.execute('''SELECT product_id FROM product;''')
    return [int(id_[0]) for id_ in cursor.fetchall()]


async def create_order(customer_id: int, first_product_price: int) -> int:
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
                              ({customer_id}, {first_product_price}.00, 'PENDING');''')
            connection.commit()
    return id_


async def create_customer(customer_id: int, name: str, phone: str):
    '''creates customer in db'''
    cursor.execute(f'''INSERT INTO customer 
                      (customer_id, name, phone)
                      VALUES 
                      ({customer_id}, '{name}', '{phone}');''')
    connection.commit()


async def create_orderitem(order_id: int, product_id: int, price: float):
    '''creates an orderitem record in db'''
    cursor.execute(f'''SELECT quantity FROM orderitem WHERE
                      order_id = {order_id} AND product_id = {product_id};''')
    quantity = cursor.fetchone()
    print(quantity)
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
