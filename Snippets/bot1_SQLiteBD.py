import asyncio

import aiogram.utils.markdown as md
import Keyboards
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from SQLite3_DB_for_bot import db_table, select_id_column, report_column
from functions_for_bot import checking_date
from config import BOT_TOKEN


storage = MemoryStorage()
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    email = State()
    birthday = State()


@dp.message_handler(commands=['todb'])
async def testing_db(message: types.Message):
    await Form.email.set()
    await message.answer(text="Insert your full email:")


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer(text='Ok.')


@dp.message_handler(state=Form.email)
async def process_email(message: types.Message, state: FSMContext):
    emails_ls = ['gmail.com', 'mail.ru', 'yandex.ru', 'owa.mos.ru']
    if '@' in message.text and message.text.split('@')[1] in emails_ls:
        async with state.proxy() as data:
            data['email'] = message.text
        await Form.next()
        await message.answer(text="Insert your birth date in 'YYYY-MM-DD' format:")
    else:
        await Form.email.set()
        await bot.send_message(chat_id=message.chat.id,
                               text="Insert your real full email\!\n"
                                    "It must ending with *@_'your\_provider'_*",
                               parse_mode=types.ParseMode.MARKDOWN_V2)


@dp.message_handler(state=Form.birthday)
async def process_email(message: types.Message, state: FSMContext):
    if not checking_date(message.text):
        await Form.birthday.set()
        await bot.send_message(chat_id=message.chat.id,
                               text="Only *'YYYY-MM-DD'* input format is available,"
                                    "for example _1900-12-31_\!",
                               parse_mode=types.ParseMode.MARKDOWN)
    else:
        async with state.proxy() as data:
            data['birthday'] = message.text

            us_id = message.from_user.id
            us_name = message.from_user.first_name
            us_surname = message.from_user.last_name
            username = message.from_user.username
            email = data['email']
            b_day = data['birthday']

        await bot.send_message(chat_id=message.chat.id,
                               text=md.text(
                                   email,
                                   b_day,
                                   # md.text('Hi\! Nice to meet you\,', md.bold(data['email'])),
                                   # md.text('YES\,', md.bold(data['birthday'])),
                                   sep='\n',
                                    ),
                               )

        if select_id_column('user_id') is None or int(us_id) not in select_id_column('user_id'):
            db_table(user_id=us_id, user_name=us_name, user_surname=us_surname,
                     username=username, email=email, b_day=b_day)
            await bot.send_message(chat_id=message.chat.id,
                                   text="*Your data writen down into table\.*",
                                   parse_mode=types.ParseMode.MARKDOWN_V2)
        else:
            await bot.send_message(chat_id=message.chat.id,
                                   text="Your data is *already exist* in DB\!",
                                   parse_mode=types.ParseMode.MARKDOWN_V2)
        await state.finish()
        await asyncio.sleep(2)
        await bot.send_message(chat_id=message.chat.id,
                               text='Do you want get list of users names?',
                               reply_markup=Keyboards.report_keyboard2)


@dp.message_handler(Text(['Да', 'Нет']))
async def report_answer(message: types.Message):
    if message.text == 'Да':
        await message.answer(text=report_column('user_name'),
                             reply_markup=Keyboards.ReplyKeyboardRemove())
    else:
        await message.answer(text='Ok.',
                             reply_markup=Keyboards.ReplyKeyboardRemove())

if __name__ == '__main__':
    executor.start_polling(dp)
