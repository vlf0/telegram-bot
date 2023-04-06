import logging
import random
# import pandas as pd
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, filters
from aiogram.utils import executor
from config import BOT_TOKEN, photo_abs_path, chat_id_list
from writing_in_excel import columns_list, limits

# Configure logging
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('''Hello!\nThat is 
    commands what i can done:!
    "bored" - set uo your mood 
    by animals picture!;
    ''')


@dp.message_handler(commands=['bored'])
async def process_start_command(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id,  # selected the chat where from  it was received
                         photo=open(random.choice(photo_abs_path), 'rb'),
                         caption='Take the pretty cat, enjoy!:)')


@dp.message_handler(commands=['report'])
async def reporting(message: types.Message):
    kb = [
           [
               types.KeyboardButton(text='Нормальная_еда'),
               types.KeyboardButton(text='Рынок')
               # [types.KeyboardButton(text='Маркеты')],
               # [types.KeyboardButton(text='SEVEN_ELEVEN')],
               # [types.KeyboardButton(text='Транспорт')],
               # [types.KeyboardButton(text='Прочее')]
           ],
         ]
    keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
    await bot.send_message(message.chat.id,
                           'Choose something', reply_markup=keyboard)


@dp.message_handler(filters.Text(columns_list))
async def first_var(message: types.Message):
    await message.reply('Ok, insert the sum: ',
                        reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(filters.Text(limits))
async def take_sum(message: types.Message):
    await bot.send_message(chat_id=message.chat.id,
                           text='Ok, this sum will be writen in the your table',
                           reply_to_message_id=message.message_id)


async def starting_note():
    for ch_id in chat_id_list:
        await bot.send_message(ch_id, 'Bot is starting!')


if __name__ == '__main__':
    executor.start(dp, starting_note())
    executor.start_polling(dp)

