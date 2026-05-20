import sqlite3
import json

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

def putUserToEnd(user_id, queue_id):
    conn = sqlite3.connect('src/data.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE user_id = ?', [user_id])
    result = cursor.fetchall()
    result2 = None
    if result:
        cursor.execute('SELECT * FROM queue WHERE (instr(list, ?) > 0) AND id = ?', [result[0][0], int(queue_id)])
        result2 = cursor.fetchall()
        if result2:
            queue: list = json.loads(result2[0][4])
            queue.remove(result[0][0])
            queue.append(result[0][0])
            cursor.execute('UPDATE queue SET list = ? WHERE id = ?', [json.dumps(queue), int(queue_id)])
            conn.commit()
    conn.close()

def skipOne(user_id, queue_id):
    conn = sqlite3.connect('src/data.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE user_id = ?', [user_id])
    result = cursor.fetchall()
    result2 = None
    if result:
        cursor.execute('SELECT * FROM queue WHERE (instr(list, ?) > 0) AND id = ?', [result[0][0], int(queue_id)])
        result2 = cursor.fetchall()
        if result2:
            queue: list = json.loads(result2[0][4])
            index = queue.index(result[0][0])
            if index != len(queue)-1:
                queue.insert(index, queue.pop(index+1))
            cursor.execute('UPDATE queue SET list = ? WHERE id = ?', [json.dumps(queue), int(queue_id)])
            conn.commit()
    conn.close()

def leaveQueue(user_id, queue_id):
    conn = sqlite3.connect('src/data.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE user_id = ?', [user_id])
    result = cursor.fetchall()
    result2 = None
    if result:
        cursor.execute('SELECT * FROM queue WHERE (instr(list, ?) > 0) AND id = ?', [result[0][0], int(queue_id)])
        result2 = cursor.fetchall()
        if result2:
            queue: list = json.loads(result2[0][4])
            queue.remove(result[0][0])
            cursor.execute('UPDATE queue SET list = ? WHERE id = ?', [json.dumps(queue), int(queue_id)])
            conn.commit()
    conn.close()

def kickQueue(user_id, queue_id, index):
    conn = sqlite3.connect('src/data.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE user_id = ?', [user_id])
    result = cursor.fetchall()
    result2 = None
    if result:
        cursor.execute('SELECT * FROM queue WHERE author_id = ? AND id = ?', [result[0][0], int(queue_id)])
        result2 = cursor.fetchall()
        if result2:
            queue: list = json.loads(result2[0][4])
            queue.pop(index-1)
            cursor.execute('UPDATE queue SET list = ? WHERE id = ?', [json.dumps(queue), int(queue_id)])
            conn.commit()
    conn.close()

def deleteQueue(user_id, queue_id):
    conn = sqlite3.connect('src/data.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE user_id = ?', [user_id])
    result = cursor.fetchall()
    if result:
        cursor.execute('DELETE FROM queue WHERE author_id = ? AND id = ?', [result[0][0], int(queue_id)])
        conn.commit()
    conn.close()