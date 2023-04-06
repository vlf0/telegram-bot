import pandas as pd
lim = [nums for nums in range(10000)]
limits = [str(i) for i in lim]
columns_list = ('Нормальная_еда  Рынок  Маркеты  '
           'SEVEN_ELEVEN  Транспорт  Прочее  Дудка  Одежда').split()


if __name__ == '__main__':
    df = pd.read_excel(r'C:\Users\dr_dn\Desktop\Расход средств1_test.xlsx', header=0)
    new_row = (df.count()['Маркеты'])
    print(new_row)
    print(df)
    df.at[new_row, 'Маркеты'] = '84 dfdfgdfg'
    print(df)


    #  df.to_excel(r'C:\Users\dr_dn\Desktop\Расход средств1_test.xlsx', header=True, index=False)

