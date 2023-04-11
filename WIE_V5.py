# from bot1 import column_name, sums
import pandas as pd
import datetime

columns_list = ('Нормальная_еда Рынок Маркеты  '
                'SEVEN_ELEVEN Транспорт Дудка Одежда Связь Прочее').split()


def message_text(selected_column, result):
    tab_file = r'C:\Users\dr_dn\Desktop\Расход средств1_test.xlsx'
    current_date = datetime.date.today()  # current date for compare with dates list from column
    data_frame = pd.read_excel(tab_file, header=0, engine='openpyxl')  # reading file
    df = data_frame.select_dtypes(include='datetime64')  # select a column containing dates
    dates_list = [datetime.datetime.date(data_frame.at[i, 'Дата']) for i in range(len(df))]
    cur_ind = dates_list.index(current_date)
    if current_date in dates_list:
        data_frame.at[cur_ind, selected_column] = result
        data_frame.to_excel(tab_file, header=True, index=False, engine='openpyxl')








