import sqlite3


def initiate_db():
    connection = sqlite3.Connection('database.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS Products('
                   'id INTEGER PRIMARY KEY,'
                   'title TEXT NOT NULL,'
                   'description TEXT,'
                   'price INTEGER NOT NULL)')
    connection.commit()
    cursor.close()


async def get_all_products():
    connection = sqlite3.Connection('database.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    cursor.close()
    return products


def insert_values(products: list):
    connection = sqlite3.Connection('database.db')
    cursor = connection.cursor()
    for product in products:
        cursor.execute(f'INSERT INTO Products (title, description, price) VALUES(?, ?, ?)',
                       (product[0], product[1], product[2]))
    connection.commit()
    cursor.close()


list_of_products = [('Наушники прикольные', 'Ну очень прикольные', 9000),
                    ('Наушники стильные', 'Ну очень стильные', 15000),
                    ('Наушники хит 2024', 'Их носят все', 6000),
                    ('Наушники для богатых', 'Если есть лишние деньги', 30000)]

# initiate_db()
# insert_values(list_of_products)
