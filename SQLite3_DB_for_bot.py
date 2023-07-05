import sqlite3

contact = sqlite3.connect('/home/vlf/vlf_bot/files/test_db.db3', check_same_thread=False)
cursor = contact.cursor()


def select_id_column(column_name):
    id_column = contact.execute("SELECT user_id "
                                "FROM users_data")
    ls = []
    for ch in id_column.fetchall():
        ls.append(ch[0])
    return ls


def report_column(colum_name):
    selected_column = contact.execute(f"SELECT {colum_name} "
                                      f"FROM users_data")
    st = ''
    for i in selected_column.fetchall():
        st = st + i[0] + '\n'
    return st


def db_table(user_id: int, user_name: str,
             user_surname: str, username: str,
             email: str, b_day: str):
    cursor.execute('INSERT INTO users_data '
                   '(user_id, user_name, user_surname,'
                   'username, email, b_day) '
                   'VALUES (?,?,?,?,?,date(?))',
                   (user_id, user_name, user_surname,
                    username, email, b_day))
    contact.commit()


def write_id(table, filename: str, file_id: str, hashes: str, bb, size: int, duration: int):
    id_column = contact.execute(f"SELECT hashes FROM {table}")
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
            elif table == 'photos_file_id':
                cursor.execute(f'INSERT INTO {table} '
                               f'(file_id, hashes) '
                               f'VALUES (?, ?)',
                               (file_id, hashes))
                contact.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    else:
        return False


def get_table_name():
    cursor.execute('SELECT name '
                   'FROM sqlite_master '
                   'WHERE type="table"')
    return cursor.fetchall()[1::]   # get all tables from BD


def get_photos_id():
    raw_list = cursor.execute('SELECT file_id '
                   'FROM photos_file_id')
    ls = raw_list.fetchall()
    id_ls = [ch[0] for ch in ls]
    return id_ls


def deleting_data():
    try:
        cursor.execute('DELETE FROM photos_file_id')
        contact.commit()
        return 'All data was deleted.'
    except sqlite3.Error:
        return 'Something is wrong.'

