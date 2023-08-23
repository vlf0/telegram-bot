import sqlite3

# censored words filter
keywords = ['бля', 'ебан', 'ебат', 'ёбан', 'пизд', 'пидор', 'пидар']


def text():
    return


def select_id_column(column_name):
    contact = sqlite3.connect(r'C:\Users\dr_dn\Desktop\test_db.db3', check_same_thread=False)
    cursor = contact.cursor()
    id_column = cursor.execute('SELECT user_id '
                               'FROM users_data')
    ls = []
    for ch in id_column.fetchall():
        ls.append(ch[0])
    contact.close()
    return ls


def report_column(colum_name):
    contact = sqlite3.connect(r'C:\Users\dr_dn\Desktop\test_db.db3', check_same_thread=False)
    cursor = contact.cursor()
    selected_column = cursor.execute(f'SELECT {colum_name} '
                                     f'FROM users_data')
    st = ''
    for i in selected_column.fetchall():
        st = st + i[0] + '\n'
    contact.close()
    return st


# record TG users ids to DB for checking for violations chat rules
def users_tracking(user_id, username, name, surname, message_id):
    contact = sqlite3.connect(r'C:\Users\dr_dn\Desktop\test_db.db3', check_same_thread=False)
    cursor = contact.cursor()
    try:
        cursor.execute('CREATE TABLE IF NOT EXISTS ban_list '
                       '(ID INTEGER PRIMARY KEY AUTOINCREMENT, '
                       'user_id INTEGER UNIQUE, '
                       'username TEXT, '
                       'name TEXT, '
                       'surname TEXT, '
                       'notified INTEGER, '
                       'message_id INTEGER UNIQUE)'
                       )
        # insert user data to db
        cursor.execute('INSERT INTO ban_list '
                       '(user_id, username, name, surname, notified, message_id) '
                       f'VALUES (?,?,?,?,{1},?)',
                       (user_id, username, name, surname, message_id)
                       )
        contact.commit()
        contact.close()
        return 1
    # if user already exists we check in table
    except sqlite3.IntegrityError:
        cursor.execute('SELECT notified '
                       'FROM ban_list '
                       f'WHERE user_id = {user_id}'
                       )
        # notices value (3 maximum)
        notice = cursor.fetchone()[0]
        if notice == 1:
            notice += 1
            cursor.execute('UPDATE ban_list '
                           f'SET notified = {notice}'
                           )
            contact.commit()
            contact.close()
            return notice
        elif notice == 2:
            notice += 1
            cursor.execute('UPDATE ban_list '
                           f'SET notified = {notice}'
                           )
            contact.commit()
            contact.close()
            return notice
        else:
            contact.close()
            return 'Banned'


def db_table(user_id: int, user_name: str,
             user_surname: str, username: str,
             email: str, b_day: str):
    contact = sqlite3.connect(r'C:\Users\dr_dn\Desktop\test_db.db3', check_same_thread=False)
    cursor = contact.cursor()
    cursor.execute('INSERT INTO users_data '
                   '(user_id, user_name, user_surname,'
                   'username, email, b_day) '
                   'VALUES (?,?,?,?,?,date(?))',
                   (user_id, user_name, user_surname,
                    username, email, b_day))
    contact.commit()
    contact.close()


def write_id(table, filename: str, file_id: str, hashes: str, bb, size: int, duration: int):
    contact = sqlite3.connect(r'C:\Users\dr_dn\Desktop\test_db.db3', check_same_thread=False)
    cursor = contact.cursor()
    id_column = contact.execute(f'SELECT hashes FROM {table}')
    ls = []
    for ch in id_column.fetchall():
        ls.append(ch[0])
    if hashes not in ls:
        try:
            if table == 'music':
                cursor.execute(f'INSERT INTO {table} '
                               f'(filename, file_id, hashes, bb, size, duration) '
                               f'VALUES (?, ?, ?, ?, ?, ?)', (filename, file_id, hashes, bb, size, duration))
                contact.commit()
                contact.close()
            elif table == 'photos_file_id':
                cursor.execute(f'INSERT INTO {table} '
                               f'(file_id, hashes) '
                               f'VALUES (?, ?)',
                               (file_id, hashes))
                contact.commit()
                contact.close()
            return True
        except sqlite3.IntegrityError:
            contact.close()
            return False
    else:
        contact.close()
        return False


def get_table_name():
    contact = sqlite3.connect(r'C:\Users\dr_dn\Desktop\test_db.db3', check_same_thread=False)
    cursor = contact.cursor()
    cursor.execute('SELECT name '
                   'FROM sqlite_master '
                   'WHERE type="table"')
    tabs = cursor.fetchall()[1::]  # get all tables from BD
    contact.close()
    return tabs


def get_photos_id():
    contact = sqlite3.connect(r'C:\Users\dr_dn\Desktop\test_db.db3', check_same_thread=False)
    cursor = contact.cursor()
    raw_list = cursor.execute('SELECT file_id '
                              'FROM photos_file_id')
    ls = raw_list.fetchall()
    id_ls = [ch[0] for ch in ls]
    contact.close()
    return id_ls


def deleting_data():
    contact = sqlite3.connect(r'C:\Users\dr_dn\Desktop\test_db.db3', check_same_thread=False)
    cursor = contact.cursor()
    try:
        cursor.execute('DELETE FROM photos_file_id')
        contact.commit()
        contact.close()
        return 'All data was deleted.'
    except sqlite3.Error:
        contact.close()
        return 'Something is wrong.'



