import aiogram.utils.markdown as md
import random
import logging
import Keyboards
from asyncio import sleep
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from SQLite3_DB_for_bot import db_table, select_id_column, report_column
from config import BOT_TOKEN, cat_photo, chat_id_list, welcome_picture
from functions_for_bot import checking_date
from WIE2 import columns_list, message_text


storage = MemoryStorage()
column_name = []
sums = []
# Configure logging
logging.basicConfig(level=logging.INFO)
bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.MARKDOWN_V2)
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    email = State()
    birthday = State()
    cn_nm = State()
    sm = State()

@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer_photo(photo=open(welcome_picture, 'rb'), caption='*Sounds of joy*')
    await sleep(1)
    await message.answer('*WARNING\!*\nFor now Insert sums '
                         'after command *_report_* only\!')


@dp.message_handler(commands=['bored'])
async def process_start_command(message: types.Message):
    await bot.send_photo(chat_id=message.chat.id,  # selected the chat where from  it was received
                         photo=open(random.choice(cat_photo), 'rb'),
                         caption='Enjoy!\n:)', parse_mode='')


@dp.message_handler(commands='location')
async def send_location(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text='Send your geo.', reply_markup=Keyboards.geo_keyboard,
                           parse_mode='')


@dp.message_handler(commands=['report'])
async def reporting(message: types.Message):
    if message.chat.id in chat_id_list:
        await Form.cn_nm.set()
        await bot.send_message(chat_id=message.chat.id, text='*Choose something:*',
                               reply_markup=Keyboards.report_keyboard)
    else:
        await bot.send_message(chat_id=message.chat.id, text='Sorry, this command is not allowed for you.',
                               parse_mode='')


@dp.message_handler(commands=['todb'])
async def testing_db(message: types.Message):
    await Form.email.set()
    await message.answer(text="Insert your full email:", parse_mode='')


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(filters.Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer(text='Ok, exiting.', parse_mode='')


@dp.message_handler(state=Form.email)
async def process_email(message: types.Message, state: FSMContext):
    emails_ls = ['gmail.com', 'mail.ru', 'yandex.ru', 'owa.mos.ru']
    if '@' in message.text and message.text.split('@')[1] in emails_ls:
        async with state.proxy() as data:
            data['email'] = message.text
        await Form.next()
        await message.answer(text="Insert your birth date in *'YYYY\-MM\-DD'* format:")
    else:
        await Form.email.set()
        await bot.send_message(chat_id=message.chat.id,
                               text="Insert your real full email\!\n"
                                    "It must ending with *@ _'your\_provider'_*")


@dp.message_handler(state=Form.birthday)
async def process_email(message: types.Message, state: FSMContext):
    if not checking_date(message.text):
        await Form.birthday.set()
        await bot.send_message(chat_id=message.chat.id,
                               text="Only *'YYYY\-MM\-DD'* input format is available, "
                                    "for example _1900\-12\-31_\!")
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
                               parse_mode=''
                               )

        if select_id_column('user_id') is None or int(us_id) not in select_id_column('user_id'):
            db_table(user_id=us_id, user_name=us_name, user_surname=us_surname,
                     username=username, email=email, b_day=b_day)
            await bot.send_message(chat_id=message.chat.id,
                                   text="*Your data writen down into table\.*")
        else:
            await bot.send_message(chat_id=message.chat.id,
                                   text="Your data is *already exist* in DB\!")
        await state.finish()
        await sleep(2)
        await bot.send_message(chat_id=message.chat.id,
                               text='Do you want get list of users names?',
                               reply_markup=Keyboards.report_keyboard2,
                               parse_mode='')


@dp.message_handler(filters.Text(['Да', 'Нет']))
async def report_answer(message: types.Message):
    if message.text == 'Да':
        await message.answer(text=report_column('user_name'),
                             reply_markup=Keyboards.ReplyKeyboardRemove())
    else:
        await message.answer(text='Ok.',
                             reply_markup=Keyboards.ReplyKeyboardRemove(),
                             parse_mode='')


@dp.message_handler(commands=['rmKeyboard'])
async def removing_keyboards(message: types.Message):
    await message.answer(text='*Removing all keyboards\.*',
                         reply_markup=Keyboards.ReplyKeyboardRemove())


@dp.message_handler(filters.Text(columns_list), state=Form.cn_nm)
async def first_var(message: types.Message, state: FSMContext):
    global column_name
    column_name = message.text
    if column_name == 'Прочее':
        await message.reply(text="*NOTE\!\nDon\\'t forget write down comment about that sum\!*\n"
                                 "_To do it Choose \\'Комменты\\' column by button below  and insert text\._\n\n"
                                 "Insert the sum: ",
                            reply_markup=Keyboards.comment_keyboard)
    elif column_name == 'Комменты':
        await message.answer(text='*Insert text value (comment)*: ')
    else:
        async with state.proxy() as data:
            data['cn_nm'] = column_name
        await Form.next()
        await message.answer(text='*Insert the sum:* ')


@dp.message_handler(state=Form.sm)
async def take_sum(message: types.Message, state: FSMContext):
    global sums
    if message.text.isdigit():
        sums = message.text
        async with state.proxy() as data:
            data['sm'] = sums
        message_text(column_name, sums)
        await state.finish()
        await bot.send_message(chat_id=message.chat.id,
                               text=md.text('_Ok, this sum_', sums, '_was writen into_', column_name),
                               reply_to_message_id=message.message_id,
                               reply_markup=Keyboards.ReplyKeyboardRemove())
    elif message.text.isalpha():
        sums = message.text
        message_text(column_name, sums)
        await bot.send_message(chat_id=message.chat.id,
                               text='_Ok, this comment was writen into "Комменты" column\._')


async def starting_note():
    owners = 406086387
    await bot.send_message(chat_id=owners, text='*Bot is starting\!*')


if __name__ == '__main__':
    executor.start(dp, starting_note())
    executor.start_polling(dp)
