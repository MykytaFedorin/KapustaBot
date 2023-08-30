import psycopg2 as psql

connection = psql.connect("dbname=myshop user=nikita")
cursor = connection.cursor()

def create_customer(telegram_id: int, name: str, phone: str):
    '''Create a record with customer info'''
    cursor.execute(f'''INSERT INTO customer 
                      (telegram_id, name, phone)
                      VALUES ({telegram_id}, '{name}', '{phone}');''');
    connection.commit()


create_customer(2, 'Nikita', '+421949175898')
