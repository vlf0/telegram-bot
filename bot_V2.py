import logging
import random

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import BOT_TOKEN, photo_abs_path, chat_id_list

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
    await bot.send_document(chat_id=message.from_user.id,
                            document=open(r'C:\Users\dr_dn\Desktop\Расход средств.xlsx', 'rb'))

@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.chat.id, msg.text)


async def starting_note():
    for ch_id in chat_id_list:
        await bot.send_message(ch_id, 'Bot is starting!')


if __name__ == '__main__':
    executor.start(dp, starting_note())
    executor.start_polling(dp)

