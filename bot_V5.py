from asyncio import sleep
import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, filters
from aiogram.utils import executor
from config import BOT_TOKEN, random_photo, chat_id_list, welcome_picture
from WIE2 import columns_list, message_text
from Keyboards import keyboard

column_name = []
sums = []
# Configure logging
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer_photo(welcome_picture, '*Sounds of joy*')
    await sleep(1)
    await message.answer('WARNING!\nFor now Insert sums '
                         'after command "report" only!')


@dp.message_handler(commands=['bored'])
async def process_start_command(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id,  # selected the chat where from  it was received
                         photo=random_photo,
                         caption='Take the pretty cat, enjoy!:)')


@dp.message_handler(commands=['report'])
async def reporting(message: types.Message):
    await bot.send_message(message.chat.id,
                           'Choose something', reply_markup=keyboard)


@dp.message_handler(filters.Text(columns_list))
async def first_var(message: types.Message):
    global column_name
    column_name = message.text
    await message.answer(text='Ok, insert the sum: ')


@dp.message_handler(filters.IsReplyFilter(is_reply=True))
async def take_sum(message: types.Message):
    if message.text.isdigit():
        global sums
        sums = message.text
        await bot.send_message(chat_id=message.chat.id,
                               text='Ok, this sum will be writen in the your table',
                               reply_to_message_id=message.message_id)
        message_text(column_name, sums)
    else:
        await bot.send_message(chat_id=message.chat.id, text='Please, insert only nums!')


async def starting_note():
    for ch_id in chat_id_list:
        await bot.send_message(chat_id=ch_id, text='Bot is starting!')


if __name__ == '__main__':
    executor.start(dp, starting_note())
    executor.start_polling(dp)
