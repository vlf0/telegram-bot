import logging
import random

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from config import BOT_TOKEN, photo_abs_path

# Configure logging
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply('Привет!\nНапиши что-нибудь!')

@dp.message_handler(commands=['help'])
async def process_start_command(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id,  # selected the chat where from  it was received
                         photo=open(random.choice(photo_abs_path), 'rb'), \
                         caption='Take the pretty cat, enjoy!:)')

@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text)

if __name__ == '__main__':
    executor.start_polling(dp)
