import os
import hashlib
import random
import string
import requests
from datetime import datetime


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


def reminded_seconds():  # count reminded days or seconds
    month_days = {1: 30, 2: 28, 3: 30, 4: 31, 5: 30, 6: 31,
                  7: 30, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}

    seconds_pd = 86400
    month = datetime.today().month
    day = 30  # datetime.today().day
    days_in = month_days[month]
    if day != days_in:
        return days_in - day
    elif day == days_in:
        cur_seconds = datetime.now().time()
        sec_hour = cur_seconds.hour * 3600
        sec_minute = cur_seconds.minute * 60
        sec = cur_seconds.second
        seconds_sum = sec_hour + sec_minute + sec
        result = seconds_pd - seconds_sum
        return result


def get_file():  # download excel from my pythonanywhere acc and save to local
    host = "www.pythonanywhere.com"
    token = 'be130000bf73cdfecd90171b274ea0053d6d6033'
    us_name = 'vlf'
    dd_path = '/home/vlf/vlf_bot/files/spents.xlsx'
    r = requests.get('https://{host}/api/v0/user/{username}/files'
                     '/path{path}'.format(host=host, username=us_name, path=dd_path),
                     headers={'Authorization': 'Token {token}'.format(token=token)})
    ud_path = r'D:\Загрузки\spents.xlsx'
    with open(ud_path, 'wb') as f:
        f.write(r.content)
    return ud_path


def to_binary(filename):  # change data type to binary
    with open(filename, 'rb') as dwn_photo:
        blob_data = dwn_photo.read()
    with open(filename, 'rb') as for_hash:  # finding hash from binary file
        hsh = hashlib.sha1()  # create var - method encrypt
        while True:
            data = for_hash.read(128)  # why 128? what different?
            if not data:
                break
            hsh.update(data)  # update hash all bytes data
        res = hsh.hexdigest()  # var which containing view in alphabetic symbols
    return blob_data, res  # hash and then binary data file for writing into tab


def rand_name():  # create random string by its length = 10
    lenn = 10
    rdy_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=lenn))
    return str(rdy_name)


def get_file_size(file_path):
    fl_size = (os.stat(file_path).st_size / 1024) / 1024
    mb_size = '{:.2}'.format(fl_size) + ' mb'
    return mb_size
