import pandas as pd
import datetime
import math

columns_list = ('Нормальная_еда Рынок Маркеты  '
                'SEVEN_ELEVEN Транспорт Дудка '
                'Одежда Связь Велики Алкоголь '
                'Здоровье Прочее Комменты'
                ).split()
tab_file = '/home/vlf/vlf_bot/static_files/spents.xlsx'
columns_list3 = ['Нормальная еда', 'Рынок', 'Маркеты', 'SEVEN ELEVEN',
                 'Транспорт', 'Дудка', 'Одежда', 'Связь', 'Велики',
                 'Алкоголь', 'Здоровье', 'Прочее', 'Комменты'
                 ]
cl3 = columns_list3.copy()
cl3.remove(columns_list3[-1])


def local_datetime():
    local_time = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
    current_month = datetime.date.strftime(local_time, '%B')
    current_date = datetime.datetime.date(local_time)
    data = {'lc': local_time, 'month': current_month, 'date': current_date}
    return data


def message_text(selected_column, result):
    data_frame = pd.read_excel(tab_file, sheet_name=None, dtype={'Комменты': 'str'}, engine='openpyxl')
    sheets = list(data_frame.keys())
    df = data_frame[local_datetime()['month']].select_dtypes(include='datetime64')  # select a column containing dates
    dates_list = [datetime.datetime.date(data_frame[local_datetime()['month']].at[i, 'Дата']) for i in range(len(df))]
    current_ind = dates_list.index(local_datetime()['date'])
    if local_datetime()['date'] in dates_list:
        if selected_column == 'Комменты':
            if type(data_frame[local_datetime()['month']].at[current_ind, selected_column]) is float:
                data_frame[local_datetime()['month']].at[current_ind, selected_column] = str(result)
            elif type(data_frame[local_datetime()['month']].at[current_ind, selected_column]) is str:
                data_frame[local_datetime()['month']].at[current_ind, selected_column] += '; ' + str(result)
        else:
            if math.isnan(data_frame[local_datetime()['month']].at[current_ind, selected_column]):
                data_frame[local_datetime()['month']].at[current_ind, selected_column] = int(result)
            elif math.isfinite(data_frame[local_datetime()['month']].at[current_ind, selected_column]):
                data_frame[local_datetime()['month']].at[current_ind, selected_column] += int(result)
    with pd.ExcelWriter(tab_file, mode='w', engine='xlsxwriter', datetime_format='d mmm',
                        date_format='d mmm') as wb:
        for m in sheets:
            data_frame[m].to_excel(wb, sheet_name=m, header=True, index=False)


def cnt_month():
    double_lists = []
    result = ''
    comments = ''
    data_frame = pd.read_excel(tab_file, sheet_name=local_datetime()['month'],
                               dtype={'Комменты': 'str'},
                               engine='openpyxl')
    dates_list = [datetime.datetime.date(data_frame.at[i, 'Дата']) for i in range(len(data_frame['Дата']))]
    current_ind = dates_list.index(local_datetime()['date'])
    strings_sum = data_frame[cl3].sum().to_list()
    for i_ind, i in enumerate(strings_sum):
        string_markup = {
            0: (' ' * 5),       1: (' ' * 25),      2: (' ' * 20),      3: (' ' * 10),
            4: (' ' * 17),      5: (' ' * 26),      6: (' ' * 22),      7: (' ' * 26),
            8: (' ' * 23),      9: (' ' * 19),      10: (' ' * 18),     11: (' ' * 22)
        }
        if not math.isnan(strings_sum[i_ind]):
            double_lists.append([cl3[i_ind], str(int(strings_sum[i_ind]))])
        elif math.isnan(strings_sum[i_ind]):
            double_lists.append([cl3[i_ind], '0'])
        # result = result + double_lists[i_ind][0] + string_markup[i_ind] + double_lists[i_ind][1] + '\n'
        result = f'{result}{double_lists[i_ind][0]}{string_markup[i_ind]}{double_lists[i_ind][1]}\n'

    for i in range(0, current_ind+1):
        try:
            comments = comments + data_frame.at[i, 'Комменты'] + ';  '
        except TypeError:
            comments = comments + ''
    double_lists.append([columns_list3.copy().pop(), comments])
    # result = result + double_lists[-1][0] + (' ' * 17) + comments + '\n'
    result = f'{result}{double_lists[-1][0]}{(" "  * 17)}{comments}\n'
    # exa = [(ex + data_frame.at[i, 'Комменты'] + ';  ' for i in range(0, current_ind+1)) if type(i) is str else ex + '']
    result_sum = str(int(data_frame[cl3].sum().sum()))
    if len(result_sum) == 1:
        result_sum = '{:>17}'.format(*result_sum)
    else:
        result_sum = ('{:>17}' + '{:>0}' * (len(result_sum) - 1)).format(*result_sum)
    return result + ('_'*32) + '\n' + 'Summary:  ' + result_sum


def cnt_day():
    double_lists = []
    result = ''
    data_frame = pd.read_excel(tab_file, sheet_name=local_datetime()['month'],
                               dtype={'Комменты': 'str'},
                               engine='openpyxl')
    dates_list = [datetime.datetime.date(data_frame.at[i, 'Дата']) for i in range(len(data_frame['Дата']))]
    current_ind = dates_list.index(local_datetime()['date'])
    strings_sum = data_frame[columns_list3].loc[current_ind]
    strings_sum = strings_sum.to_list()
    for i_ind, i in enumerate(strings_sum):
    # for i in strings_sum:
    #     i_ind = strings_sum.index(i)  # THIS IS FUCKING WRONG!
                                        # this will always return the index of the first occurrence of i,
                                        # not the current one.
        string_markup = {
            0: (' ' * 5),       1: (' ' * 25),      2: (' ' * 20),      3: (' ' * 10),
            4: (' ' * 17),      5: (' ' * 26),      6: (' ' * 22),      7: (' ' * 26),
            8: (' ' * 23),      9: (' ' * 19),      10: (' ' * 18),     11: (' ' * 22),
            12: (' ' * 17)
        }

        if isinstance(strings_sum[i_ind], str):
            double_lists.append([columns_list3[i_ind], data_frame.at[current_ind, 'Комменты']])
        else:
            if not math.isnan(strings_sum[i_ind]):
                double_lists.append([columns_list3[i_ind], str(int(strings_sum[i_ind]))])
            elif math.isnan(strings_sum[i_ind]):
                double_lists.append([columns_list3[i_ind], '0'])
        # result = result + double_lists[i_ind][0] + string_markup[i_ind] + double_lists[i_ind][1] + '\n'
        result = f"{result}{double_lists[i_ind][0]}{string_markup[i_ind]}{double_lists[i_ind][1]}\n"
    result_sum = str(int(data_frame[cl3].loc[current_ind].sum()))
    if len(result_sum) == 1:
        result_sum = '{:>17}'.format(*result_sum)
    else:
        result_sum = ('{:>17}' + '{:>0}' * (len(result_sum) - 1)).format(*result_sum)
    return result + ('_'*32) + '\n' + 'Summary:  ' + result_sum


def delete_data(column):
    """ Helps to delete today's data from selected column via bot's command. """

    data_frame = pd.read_excel(tab_file, sheet_name=None)
    sheets = list(data_frame.keys())
    current_sheet = data_frame[local_datetime()['month']]
    ind = current_sheet[current_sheet['Дата'] == local_datetime()['date'].strftime('%Y-%m-%d %X')].index.values[0]
    current_sheet.at[ind, column] = None
    with pd.ExcelWriter(tab_file, mode='w', engine='xlsxwriter',
                        datetime_format='d mmm',
                        date_format='d mmm') as wb:
        for m in sheets:
            data_frame[m].to_excel(wb, sheet_name=m, header=True, index=False)

