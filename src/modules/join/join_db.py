import sqlite3
import json

class RepeatJoinError(Exception):
    pass

class InvalidCodeError(Exception):
    pass

class UnknownUserError(Exception):
    pass

def joinQueue(user_id, code):
    conn = sqlite3.connect('src/data.db', check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute('SELECT id FROM users WHERE user_id = ?', [user_id])
    result = cursor.fetchall()

    if not result:
        conn.close()
        raise UnknownUserError

    user_id_our = result[0][0]
    cursor.execute('SELECT id, list FROM queue WHERE code = ?', [code])
    data = cursor.fetchall()

    if not data:
        conn.close()
        raise InvalidCodeError

    id_queue = data[0][0]
    list_queue = data[0][1]
    list_queue = json.loads(list_queue)

    if user_id_our in list_queue:
        conn.close()
        raise RepeatJoinError

    list_queue.append(user_id_our)
    list_queue = json.dumps(list_queue)

    cursor.execute('UPDATE queue SET list = ? WHERE id = ?', [list_queue, id_queue])
    conn.commit()
    conn.close()
