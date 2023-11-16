from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from WIE2 import columns_list3

kb_set1 = [
    [
        KeyboardButton(text=columns_list3[0]),
    ],
    [
        KeyboardButton(text=columns_list3[1]),
        KeyboardButton(text=columns_list3[2]),
        KeyboardButton(text=columns_list3[3]),
    ],
    [
        KeyboardButton(text=columns_list3[4]),
        KeyboardButton(text=columns_list3[5]),
        KeyboardButton(text=columns_list3[6]),
    ],
    [
        KeyboardButton(text=columns_list3[7]),
        KeyboardButton(text=columns_list3[8]),
        KeyboardButton(text=columns_list3[9]),
    ],
    [
        KeyboardButton(text=columns_list3[10]),
        KeyboardButton(text=columns_list3[11]),
        KeyboardButton(text=columns_list3[12]),
    ],
    [
        KeyboardButton(text=columns_list3[13]),
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


kb_set5 = [
            [
             KeyboardButton(text='Get day report'),
             KeyboardButton(text='Get current month report'),
             KeyboardButton(text='Get full tab'),
             ],

            [
             KeyboardButton(text='Write data in report'),
             ],

            [
             KeyboardButton(text='Delete today\'s data'),
             ],
           ]
report_keyboard3 = ReplyKeyboardMarkup(keyboard=kb_set5, resize_keyboard=True, one_time_keyboard=True)

simple_set = [[KeyboardButton(text='Add'), KeyboardButton(text='Do not add'), ], ]
choice_kb = ReplyKeyboardMarkup(keyboard=simple_set, resize_keyboard=True,
                                one_time_keyboard=True)
