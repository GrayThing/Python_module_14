import sqlite3


list_of_products = [('Наушники прикольные', 'Ну очень прикольные', 9000),
                    ('Наушники стильные', 'Ну очень стильные', 15000),
                    ('Наушники хит 2024', 'Их носят все', 6000),
                    ('Наушники для богатых', 'Если есть лишние деньги', 30000)]


def initiate_db():
    connection = sqlite3.Connection('database_14_5.db')
    cursor = connection.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS Products('
                   'id INTEGER PRIMARY KEY,'
                   'title TEXT NOT NULL,'
                   'description TEXT,'
                   'price INTEGER NOT NULL)')
    cursor.execute('CREATE TABLE IF NOT EXISTS Users('
                   'id INTEGER PRIMARY KEY,'
                   'username TEXT NOT NULL,'
                   'email TEXT NOT NULL,'
                   'age INTEGER NOT NULL,'
                   'balance INTEGER NOT NULL)')
    connection.commit()
    cursor.close()


async def get_all_products():
    connection = sqlite3.Connection('database_14_5.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM Products')
    products = cursor.fetchall()
    cursor.close()
    return products


def insert_products(products: list):
    connection = sqlite3.Connection('database_14_5.db')
    cursor = connection.cursor()
    for product in products:
        cursor.execute('INSERT INTO Products (title, description, price) VALUES(?, ?, ?)',
                       (product[0], product[1], product[2]))
    connection.commit()
    cursor.close()


async def add_user(username, email, age, balance=1000):
    connection = sqlite3.Connection('database_14_5.db')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)',
                   (username, email, age, balance))
    connection.commit()
    cursor.close()


async def is_included(username):
    connection = sqlite3.Connection('database_14_5.db')
    cursor = connection.cursor()
    flag = cursor.execute('SELECT username FROM Users WHERE username = ?', (username,)).fetchone()
    cursor.close()
    if flag:
        return True
    return False

initiate_db()
insert_products(list_of_products)