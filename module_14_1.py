import sqlite3

connection = sqlite3.Connection('no_telegram.db')
cursor = connection.cursor()

cursor.execute('CREATE TABLE IF NOT EXISTS Users('
               'id INTEGER PRIMARY KEY,'
               'username TEXT NOT NULL,'
               'email TEXT NOT NULL,'
               'age INTEGER,'
               'balance INTEGER NOT NULL)')

for i in range(1, 11):
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES(?, ?, ?, ?)',
                   (f'User{i}', f'example{i}@gmail.com', f'{i * 10}', '1000'))
    if i % 2 == 1:
        cursor.execute('UPDATE Users SET balance = ? WHERE id = ?', ('500', f'{i}'))

for i in range(1, 11):
    if i == 1 or (i - 1) % 3 == 0:
        cursor.execute('DELETE FROM Users WHERE id = ?', (f'{i}', ))

cursor.execute('SELECT username, email, age, balance FROM Users')

data = cursor.fetchall()

for row in data:
    print(f'Имя: {row[0]} | Почта: {row[1]} | Возраст: {row[2]} | Баланс: {row[3]}')

connection.commit()
cursor.close()
