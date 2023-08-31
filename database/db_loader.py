import psycopg2 as psql
from typing import NamedTuple
from aiogram.types import InputFile
connection = psql.connect("dbname=myshop user=nikita")
cursor = connection.cursor()

class Product(NamedTuple):
    name: str
    description: str
    price: float
    photo: InputFile
    available_amount: int

def create_customer(telegram_id: int, name: str, phone: str):
    '''Create a record with customer info'''
    cursor.execute(f'''INSERT INTO customer 
                      (telegram_id, name, phone)
                      VALUES ({telegram_id}, '{name}', '{phone}');''');
    connection.commit()


async def get_products() -> list[Product]:
    '''return all products available to buy
       in the form of Product objects'''
    products_wrapped = list()
    cursor.execute('''SELECT name, description, price, image_url, amount
                   FROM product;''')
    products_raw = cursor.fetchall()
    for product in products_raw:
        products_wrapped.append(Product(name = product[0],
                                        description = product[1],
                                        price = product[2], 
                                        photo = InputFile(product[3]), 
                                        available_amount = product[4]))
    return products_wrapped 

