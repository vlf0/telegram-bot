from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from WIE2 import columns_list

kb_set1 = [
    [
        KeyboardButton(text=columns_list[0]),
        KeyboardButton(text=columns_list[1]),
        KeyboardButton(text=columns_list[2]),
    ],
    [
        KeyboardButton(text=columns_list[3]),
        KeyboardButton(text=columns_list[4]),
        KeyboardButton(text=columns_list[5]),
    ],
    [
        KeyboardButton(text=columns_list[6]),
        KeyboardButton(text=columns_list[7]),
        KeyboardButton(text=columns_list[8]),
    ],
     ]

report_keyboard = ReplyKeyboardMarkup(keyboard=kb_set1, resize_keyboard=True,
                                      one_time_keyboard=True)

kb_set2 = [[KeyboardButton(text='My current location', request_location=True), ], ]
geo_keyboard = ReplyKeyboardMarkup(keyboard=kb_set2, resize_keyboard=True, one_time_keyboard=True)

kb_set3 = [[KeyboardButton(text='Комменты'), ], ]
comment_keyboard = ReplyKeyboardMarkup(keyboard=kb_set3, resize_keyboard=True, one_time_keyboard=True)

kb_set4 = [[KeyboardButton(text='Да'), KeyboardButton(text='Нет'), ], ]
report_keyboard2 = ReplyKeyboardMarkup(keyboard=kb_set4, resize_keyboard=True,
                                       one_time_keyboard=True)


