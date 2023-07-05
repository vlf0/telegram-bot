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
from SQLite3_DB_for_bot import report_column, get_table_name, write_id, get_photos_id, deleting_data
from config import BOT_TOKEN, chat_id_list
from functions_for_bot import get_file_size, to_binary
from WIE2 import columns_list3, message_text, cnt_month, cnt_day, delete_data


storage = MemoryStorage()
column_name = []
sums = []
# Configure logging
logging.basicConfig(level=logging.INFO)
PROXY_URL = "http://proxy.server:3128"


bot = Bot(token=BOT_TOKEN, proxy=PROXY_URL, parse_mode=types.ParseMode.MARKDOWN_V2)
dp = Dispatcher(bot, storage=storage)


class Form(StatesGroup):
    music_file = State()
    cn_nm_del = State()
    cn_nm = State()
    sm = State()


class Mp3Data:

    def __init__(self, filename, file_id, hashes, bb, size, duration):
        self.filename = filename
        self.file_id = file_id
        self.hashes = hashes
        self.bb = bb
        self.size = size
        self.duration = duration
        self.table = 'music'


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.answer_document(document='BQACAgIAAxkBAAIUlWRjlOXiaK4_MT35mU0EYuIXXLKvAAK7MgACmCwZS7IBecCSv8nXLwQ',
                                  caption='*Sounds of joy*')
    await sleep(1)
    await message.answer('*What can i do?*\nDescribe is below\!')


@dp.message_handler(commands=['bored'])
async def fun_command(message: types.Message):
    try:
        await bot.send_document(chat_id=message.chat.id,
                                document=random.choice(get_photos_id()))
    except IndexError:
        await bot.send_message(chat_id=message.chat.id,
                               text='BD is empty right now!',
                               parse_mode='')


@dp.message_handler(commands='delete')
async def send_location(message: types.Message):
    await bot.send_message(chat_id=message.chat.id, text=deleting_data(), parse_mode='')


@dp.message_handler(commands=['report'])
async def choice(message: types.Message):
    if message.chat.id in chat_id_list:
        await bot.send_message(chat_id=message.chat.id, text='*Choice action by button tap\:*',
                               reply_markup=Keyboards.report_keyboard3)

    else:
        await bot.send_message(chat_id=message.chat.id, text='Sorry, this command is not allowed for you.',
                               parse_mode='')


@dp.message_handler((filters.Text(['Write data in report',
                                   'Get day report',
                                   'Get current month report',
                                   'Get full tab',
                                   'Delete today\'s data'])))
async def answer_button(message: types.Message):
    if message.text == 'Get full tab':
        await bot.send_message(chat_id=message.chat.id,
                               text='Sending report for you...Done.',
                               parse_mode='', reply_markup=Keyboards.ReplyKeyboardRemove())
        await bot.send_document(chat_id=message.chat.id,
                                document=open('/home/vlf/vlf_bot/files/spents.xlsx', 'rb'),
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


@dp.message_handler(commands=['add'])
async def upload_mp3(message: types.Message):
    await Form.music_file.set()
    await message.answer(text='Send mp3 to me\.')


@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(filters.Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.answer(text='Ok, exiting.', parse_mode='')


@dp.message_handler(state=Form.music_file, content_types=types.ContentType.DOCUMENT)
@dp.message_handler(state=Form.music_file, content_types=types.ContentType.AUDIO)
async def get_mp3(message: types.Message, state: FSMContext):
    dwn_fl = r'/home/vlf/vlf_bot/files/mp3_downloaded.mp3'
    if message.content_type == 'audio' or (message.content_type == 'document'
            and message.document.mime_type == 'audio/mpeg'):
        await message.audio.download(destination_file=dwn_fl)
        ready_mp3 = Mp3Data(filename=get_table_name()[2][0],
                            file_id=message.audio.file_id,
                            hashes=to_binary(dwn_fl)[1],
                            bb=to_binary(dwn_fl)[0],
                            size=get_file_size(dwn_fl),
                            duration=message.audio.duration)
        async with state.proxy() as data:
            data['music_file'] = message.audio.file_name
            mp3_name = data['music_file']
        if write_id(table=ready_mp3.table,
                    file_id=ready_mp3.file_id,
                    filename=ready_mp3.filename,
                    hashes=ready_mp3.hashes,
                    bb=ready_mp3.bb,
                    size=ready_mp3.size,
                    duration=ready_mp3.duration):
            await state.finish()
            await bot.send_message(chat_id=message.chat.id,
                                   text=f'Your track {mp3_name} --> '
                                        f'({ready_mp3.duration} dur.) was added into your tab.',
                                   parse_mode='')
        else:
            await state.finish()
            await bot.send_message(chat_id=message.chat.id,
                                   text=f'Your track {mp3_name} --> '
                                        f'({ready_mp3.duration} dur.) already exist into your tab.',
                                   parse_mode='')
    elif message.document.mime_type != 'audio/mpeg':
        await Form.music_file.set()
        await bot.send_message(chat_id=message.chat.id,
                               text='File ext. not supported. Try again witn ".mp3" ext.',
                               parse_mode='')
    else:
        await Form.music_file.set()
        await bot.send_message(chat_id=message.chat.id,
                               text='Something went wrong. Check it.',
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
    # if message.text.isdigit():
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


@dp.message_handler(content_types=types.ContentType.DOCUMENT)
async def echo(message: types.Message):
    if message.document.mime_type == 'image/jpeg':
        file_path = r'/home/vlf/vlf_bot/files/aio_picture.png'
        await message.document.download(destination_file=file_path)
        picture_hash = to_binary(file_path)[1]
        picture = message.document.file_id
        if write_id(table='photos_file_id',
                    file_id=picture,
                    hashes=picture_hash,
                    bb=None,
                    duration=0,
                    filename='',
                    size=0):
            await bot.send_message(chat_id=message.chat.id,
                                   text='Saved to DB\.')
            # await bot.send_message(chat_id=message.chat.id,
            #                       text=picture,
            #                       parse_mode='')
        else:
            await bot.send_message(chat_id=message.chat.id,
                                   text='Already exists\.')
    else:
        await bot.send_message(chat_id=message.chat.id,
                               text='This ext\. is not supported\. Try only pictures format\.')


async def shoot_up(_):
    await bot.send_message(chat_id='406086387',
                           text='*Bot is starting\!*')


async def shoot_down(_):
    await bot.send_message(chat_id='406086387',
                           text='*I go to sleep\.*')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=shoot_up, on_shutdown=shoot_down)
