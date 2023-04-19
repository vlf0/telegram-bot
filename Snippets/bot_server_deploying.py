from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, filters
from aiogram.utils import executor
from config import chat_id_list


def give_token():
    bot_token = open(r'D:\For_path\Bot_token.txt', 'r')
    bt_text = bot_token.read()
    bot_token.close()
    return str(bt_text)


bot = Bot(token=give_token())
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def choose_user(message: types.Message):
    # a = await bot.get_chat_member_count('-1001911382719')
    a = await bot.get_chat_member(-1001911382719, 406086387)
    if message.from_id in chat_id_list:

        await bot.send_message(chat_id=message.chat.id,
                               text=a)
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text='You are not allowed access.')


@dp.message_handler(content_types=types.ContentType.TEXT)
async def echo(message: types.Message):
    await message.answer(text=message.text)


async def shoot_up():
    await bot.send_message(chat_id='406086387',
                           text='*BOT\_SERVER\_DEPLOYING'
                                ' IS START NOW*',
                           parse_mode=types.ParseMode.MARKDOWN_V2)


if __name__ == '__main__':
    executor.start(dp, shoot_up())
    executor.start_polling(dp)



