import sqlite3
import json
import random

def createQueue(queue_name, author_id):
    conn = sqlite3.connect('src/data.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE user_id = ?', [author_id])
    result = cursor.fetchall()
    if result:
        author_id_our = result[0][0]
        code = None
        while not code:
            raw_code = generateCode()
            cursor.execute('SELECT id FROM queue WHERE code = ?', [raw_code])
            base_code = cursor.fetchall()
            if not base_code:
                code = raw_code
        cursor.execute('INSERT INTO queue (name, author_id, code, list, isPublic) VALUES (?, ?, ?, ?, ?)',
                        [queue_name, author_id_our, code, json.dumps([author_id_our]), 1])
        conn.commit()
        conn.close()
        return code
    conn.close()
    return None

def generateCode():
    return random.randint(100000, 999999)