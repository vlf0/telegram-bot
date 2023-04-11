from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from WIE2 import columns_list

kb = [
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

keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True, one_time_keyboard=True)
