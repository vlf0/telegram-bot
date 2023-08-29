import datetime
import re
import aiogram.utils.markdown as md
import logging
import Keyboards
from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import executor
from config import BOT_TOKEN, chat_id_list
from WIE2 import columns_list3, message_text, cnt_month, cnt_day, delete_data
from SQLite3_DB_for_bot import keywords, users_tracking


storage = MemoryStorage()
column_name = []
sums = []
# Configure logging
logging.basicConfig(level=logging.INFO)
# PROXY_URL = "http://proxy.server:3128"


bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.MARKDOWN_V2)
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    music_file = State()
    cn_nm_del = State()
    cn_nm = State()
    sm = State()


@dp.message_handler(commands=['report'])
async def choice(message: types.Message):
    if message.chat.id in chat_id_list:
        await bot.send_message(chat_id=message.chat.id, text='*Choice action by button tap\:*',
                               reply_markup=Keyboards.report_keyboard3)
    else:
        await bot.send_message(chat_id=message.chat.id, text='Sorry, this command is not allowed for you.',
                               parse_mode='')


@dp.message_handler(filters.Text(['Write data in report',
                                  'Get day report',
                                  'Get current month report',
                                  'Get full tab',
                                  'Delete today\'s data']))
async def answer_button(message: types.Message):
    if message.text == 'Get full tab':
        await bot.send_message(chat_id=message.chat.id,
                               text='Sending report for you...Done.',
                               parse_mode='', reply_markup=Keyboards.ReplyKeyboardRemove())
        await bot.send_document(chat_id=message.chat.id,
                                document=open(r'D:\Programming\TG_bots\bot_Maxwell\static_files\spents.xlsx',
                                              'rb'),
                                parse_mode='')
    elif message.text == 'Get day report':
        await bot.send_message(chat_id=message.chat.id,
                               text='Sending report for you...Done.',
                               parse_mode='', reply_markup=Keyboards.ReplyKeyboardRemove())
        await bot.send_message(chat_id=message.chat.id, text=cnt_day(), parse_mode='')
    elif message.text == 'Get current month report':
        await bot.send_message(chat_id=message.chat.id,
                               text='Sending report for you...Done.',
                               parse_mode='', reply_markup=Keyboards.ReplyKeyboardRemove())
        await bot.send_message(chat_id=message.chat.id, text=cnt_month(), parse_mode='')
    elif message.text == 'Write data in report':
        await Form.cn_nm.set()
        await bot.send_message(chat_id=message.chat.id, text='*Choose something:*',
                               reply_markup=Keyboards.report_keyboard)
    elif message.text == 'Delete today\'s data':
        await Form.cn_nm_del.set()
        await bot.send_message(chat_id=message.chat.id, text='*Choose something:*',
                               reply_markup=Keyboards.report_keyboard)
    else:
        await bot.send_message(chat_id=message.chat.id, text='*Choose something:*',
                               reply_markup=Keyboards.ReplyKeyboardRemove())


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(filters.Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer(text='Ok, exiting.', reply_markup=Keyboards.ReplyKeyboardRemove(),
                         parse_mode='')


@dp.message_handler(commands=['rmkb'])
async def removing_keyboards(message: types.Message):
    await message.answer(text='*Removing all keyboards\.*',
                         reply_markup=Keyboards.ReplyKeyboardRemove())


@dp.message_handler(filters.Text(columns_list3), state=Form.cn_nm_del)
async def dropping(message: types.Message, state: FSMContext):
    global column_name
    column_name = message.text
    async with state.proxy() as data:
        data['cn_nm_del'] = column_name
    await state.finish()
    delete_data(column_name)
    await message.answer(text='*Today\'s data was removed from this column\.* ')


@dp.message_handler(filters.Text(columns_list3), state=Form.cn_nm)
async def first_var(message: types.Message, state: FSMContext):
    global column_name
    column_name = message.text
    async with state.proxy() as data:
        data['cn_nm'] = column_name
    await Form.next()
    await message.answer(text='*Insert the sum:* ')


@dp.message_handler(state=Form.sm)
async def take_sum(message: types.Message, state: FSMContext):
    global sums
    if column_name != "Комменты":
        sums = message.text
        async with state.proxy() as data:
            data['sm'] = sums
        message_text(column_name, sums)
        await state.finish()
        await bot.send_message(chat_id=message.chat.id,
                               text=md.text(f'_Ok, this sum_ *{sums}* _was writen'
                                            f' into_ *{column_name}*'),
                               reply_to_message_id=message.message_id,
                               reply_markup=Keyboards.ReplyKeyboardRemove())
    else:
        sums = message.text
        async with state.proxy() as data:
            data['sm'] = sums
        message_text(column_name, sums)
        await state.finish()
        await bot.send_message(chat_id=message.chat.id,
                               text=md.text('_Ok, this comment was writen into_ *Комменты* _column\._'),
                               reply_to_message_id=message.message_id,
                               reply_markup=Keyboards.ReplyKeyboardRemove())


# caught censored words from list and get ban to user
# by adding user to db and get him 2 more notice
# than they were getting ban
# @dp.message_handler(filters.Text(keywords))
# @dp.message_handler(regexp='бля')
@dp.message_handler()
async def caution(message: types.Message):
    # get filter pattern for regexp from list of censored words
    # and checking if they are in text
    for censored in keywords:
        censored_founded = re.search(censored, message.text)
        if censored_founded:
            attempts = users_tracking(user_id=message.from_user.id,
                                      username=message.from_user.username,
                                      name=message.from_user.first_name,
                                      surname=message.from_user.last_name,
                                      message_id=message.message_id
                                      )
            if attempts == 1:
                await message.reply(text='This is censored words, '
                                         'you got one notice about this\! You have __*2 more*__\.')

            elif attempts == 2:
                await message.reply(text='This is censored words, '
                                         'you got one notice about this\! You have __*1 more*__\.')
            else:
                await message.reply(text='This is censored words, '
                                         '__*you are banned*__\! You can contact to admin\.')
                await bot.ban_chat_member(chat_id=message.chat.id, user_id=message.from_user.id,
                                          until_date=datetime.timedelta(350))
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        else:
            pass


# meeting a new members and get restrict to sending messages
# until user give agree with group rules
@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def new_member(message: types.Message):
    permissions = types.ChatPermissions(can_send_messages=True)
    # this is user_id a new chat member
    new_memb = message.new_chat_members[0]["id"]
    await bot.send_message(chat_id=message.chat.id, text=f'Hello, friend! {new_memb}',
                           parse_mode='')
    await bot.restrict_chat_member(chat_id=message.chat.id,
                                   user_id=new_memb,
                                   permissions=permissions)


async def shoot_up(_):
    await bot.send_message(chat_id='406086387',
                           text='*Bot is starting\!*')


async def shoot_down(_):
    await bot.send_message(chat_id='406086387',
                           text='*I go to sleep\.*')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=shoot_up, on_shutdown=shoot_down, skip_updates=True)
