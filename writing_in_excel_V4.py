import pandas as pd
import datetime
lim = [nums for nums in range(10000)]
limits = [str(i) for i in lim]
columns_list = ('Дата Нормальная_еда  Рынок  Маркеты  '
           'SEVEN_ELEVEN  Транспорт  Прочее  Дудка  Одежда').split()


if __name__ == '__main__':
    data_frame = pd.read_excel(r'C:\Users\dr_dn\Desktop\Расход средств1_test.xlsx', header=0)
    print(data_frame)
    data_frame['Дата'] = data_frame['Дата'].astype("datetime64[ns]")
    print(data_frame.dtypes.value_counts())
    # test = data_frame.at[0, 'Дата']




    #  df.to_excel(r'C:\Users\dr_dn\Desktop\Расход средств1_test.xlsx', header=True, index=False)

