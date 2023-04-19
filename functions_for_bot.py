def checking_date(dt):
    if len(dt.split('-')[0]) == 4\
            and len(dt.split('-')[1]) == 2\
            and len(dt.split('-')[2]) == 2:
        if dt[4] == '-' and dt[7] == '-':
            b = dt.split('-')
            if b[0].isdigit() and b[1].isdigit() and b[2].isdigit():
                res = True
            else:
                res = False
            return res
        return False
    else:
        return False


# print(checking_date('200020'))
