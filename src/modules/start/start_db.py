import sqlite3

def addUser(user_id):
    conn = sqlite3.connect('src/data.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE user_id = ?', [user_id])
    result = cursor.fetchall()
    if not result:
        cursor.execute('INSERT INTO users (user_id) VALUES (?)', [user_id])
        conn.commit()
    conn.close()
