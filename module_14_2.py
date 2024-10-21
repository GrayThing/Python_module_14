import sqlite3

connection = sqlite3.Connection('not_telegram.db')
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

cursor.execute('DELETE FROM Users WHERE id = 6')
cursor.execute('SELECT COUNT(*) FROM Users')
total_users = cursor.fetchone()[0]
cursor.execute('SELECT SUM(balance) FROM Users')
all_balances = cursor.fetchone()[0]
print(all_balances / total_users)

connection.commit()
cursor.close()
