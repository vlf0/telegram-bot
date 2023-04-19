import sqlite3

contact = sqlite3.connect(r'D:\DataBases SQLite3\test_db.db3', check_same_thread=False)
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


# print(report_column('user_name'))

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
