import sqlite3

def showQueue(user_id, queue_id):
    conn = sqlite3.connect('src/data.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE user_id = ?', [user_id])
    result = cursor.fetchall()
    result2 = None
    if result:
        cursor.execute('SELECT * FROM queue WHERE (instr(list, ?) > 0 OR author_id = ?) AND id = ?', [result[0][0], result[0][0], int(queue_id)])
        result2 = cursor.fetchall()
    conn.close()
    return result2

def getTgIdById(user_id):
    conn = sqlite3.connect('src/data.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users WHERE id = ?', [user_id])
    result = cursor.fetchall()
    conn.close()
    if result:
        return result[0]
    return None