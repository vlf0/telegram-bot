from asyncio import sleep
import random
import logging
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, filters
from aiogram.utils import executor
from config import BOT_TOKEN, cat_photo, chat_id_list, welcome_picture
from WIE2 import columns_list, message_text
import Keyboards

column_name = []
sums = []
# Configure logging
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.MARKDOWN_V2)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer_photo(photo=open(welcome_picture, 'rb'), caption='*Sounds of joy*', parse_mode='')
    await sleep(1)
    await message.answer('WARNING!\nFor now Insert sums '
                         'after command "report" only!', parse_mode='')


@dp.message_handler(commands=['bored'])
async def process_start_command(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id,  # selected the chat where from  it was received
                         photo=open(random.choice(cat_photo), 'rb'),
                         caption='Take the pretty cat, enjoy!:)', parse_mode='')


@dp.message_handler(commands='location')
async def send_location(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text='Send your geo.', reply_markup=Keyboards.geo_keyboard)


@dp.message_handler(commands=['report'])
async def reporting(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text='*Choose something\:*',
                           reply_markup=Keyboards.report_keyboard)


@dp.message_handler(commands=['rmKeyboard'])
async def removing_keyboards(message: types.Message):
    await message.answer(text='*Removing all keyboards\.*',
                         reply_markup=Keyboards.ReplyKeyboardRemove())


@dp.message_handler(filters.Text(columns_list))
async def first_var(message: types.Message):
    global column_name
    column_name = message.text
    if column_name == 'Прочее':
        await message.reply(text="*NOTE\!\nDon\\'t forget write down comment about that sum\!*\n"
                                 "_To do it Choose \\'Комменты\\' column by button below  and insert text\._\n\n"
                                 "Insert the sum: ",
                            reply_markup=Keyboards.comment_keyboard)
    elif column_name == 'Комменты':
        await message.answer(text='*Insert text value \(comment\)*: ')
    else:
        await message.answer(text='*Insert the sum*: ')


@dp.message_handler(filters.IsReplyFilter(is_reply=True))
async def take_sum(message: types.Message):
    global sums
    if message.text.isdigit():
        sums = message.text
        message_text(column_name, sums)
        await bot.send_message(chat_id=message.chat.id,
                               text='_Ok, this sum was writen into your table\._',
                               reply_to_message_id=message.message_id)
    elif message.text.isalpha():
        sums = message.text
        message_text(column_name, sums)
        await bot.send_message(chat_id=message.chat.id,
                               text='_Ok, this comment was writen into "Комменты" column\._')


async def starting_note():
    for ch_id in chat_id_list:
        await bot.send_message(chat_id=ch_id, text='*Bot is starting\!*')


if __name__ == '__main__':
    executor.start(dp, starting_note())
    executor.start_polling(dp)
