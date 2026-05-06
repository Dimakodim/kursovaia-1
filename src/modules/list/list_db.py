import sqlite3

def showList(user_id):
    conn = sqlite3.connect('src/data.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE user_id = ?', [user_id])
    result = cursor.fetchall()
    result2 = None
    if result:
        cursor.execute('SELECT * FROM queue WHERE instr(list, ?) > 0 OR author_id = ?', [result[0][0], result[0][0]])
        result2 = cursor.fetchall()
    conn.close()
    return result2
