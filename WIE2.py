import pandas as pd
import datetime
import math

columns_list = ('Нормальная_еда Рынок Маркеты  '
                'SEVEN_ELEVEN Транспорт Дудка '
                'Одежда Прочее Связь Комменты').split()


def message_text(selected_column, result):
    tab_file = r'C:\Users\dr_dn\Desktop\Расход средств1_test.xlsx'
    current_date = datetime.date.today()  # current date for compare with dates list from column
    data_frame = pd.read_excel(tab_file, header=0, dtype={'Комменты': 'str'}, engine='openpyxl')  # reading file
    df = data_frame.select_dtypes(include='datetime64')  # select a column containing dates
    dates_list = [datetime.datetime.date(data_frame.at[i, 'Дата']) for i in range(len(df))]
    current_ind = dates_list.index(current_date)
    if current_date in dates_list:
        # print(data_frame.at[current_ind, selected_column])  # Checking cell output before code performance
        if selected_column == 'Комменты':
            data_frame.at[current_ind, selected_column] = str(result)
        elif math.isnan(data_frame.at[current_ind, selected_column]):
            data_frame.at[current_ind, selected_column] = int(result)
        elif math.isfinite(data_frame.at[current_ind, selected_column]):
            data_frame.at[current_ind, selected_column] += int(result)
        data_frame.to_excel(tab_file, header=True, index=False, engine='openpyxl')
        # print(type(data_frame.at[current_ind, selected_column]))   # Checking cell output after code performance






