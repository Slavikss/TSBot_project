import asyncio
import logging
import os
import shutil
from pathlib import Path
from aiogram import Bot, Dispatcher, types, executor
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, \
    InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from dotenv import load_dotenv
from processing import style_processing_cyclegan, sr_processing, style_dict, neural_transfer

# Load bot token from venv
load_dotenv('venv/token.env')

os.chdir('./')

MAX_WIDTH_SR_INPUT = 1280
MAX_HEIGHT_SR_INPUT = 720

# logging config
logging.basicConfig(filename='logs',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)

logging.info("bot logging")

logger = logging.getLogger()

# Initialize bot
bot = Bot(token=os.getenv('TOKEN'), parse_mode='HTML')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Set dict of style names of bot
style_names = {'s2w': 'Summer⇄winter(Mountain view)', 'p2m': 'Photo⇄Monet(стиль Клода Моне)',
               'p2c': 'Photo⇄Cezanne(стиль Поля Сезанна)', 'p2u': 'Photo⇄Ukiyoe(стиль изобр. искусства Японии)',
               'p2v': 'Photo⇄Vangogh(стиль Винсента Ван Гога)', 'sr': 'Повышение разрешения изображения',
               'nt': 'Собственное изображение для переноса стиля'}

# Set buttons, Keyboard markup
b1 = KeyboardButton('/Выбрать_категорию')
b2 = KeyboardButton('/Продолжить_в_этом_стиле')
kb_client = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
kb_client.add(b1)

kb = InlineKeyboardMarkup(row_width=1, one_time_keyboard=True)
kb1 = InlineKeyboardButton(text=style_names['s2w'], callback_data='s2w')
kb2 = InlineKeyboardButton(text=style_names['p2m'], callback_data='p2m')
kb3 = InlineKeyboardButton(text=style_names['p2c'], callback_data='p2c')
kb4 = InlineKeyboardButton(text=style_names['p2u'], callback_data='p2u')
kb5 = InlineKeyboardButton(text=style_names['p2v'], callback_data='p2v')
kb6 = InlineKeyboardButton(text='Собственное изображение для переноса стиля', callback_data='nt')
kb7 = InlineKeyboardButton(text='Повышение разрешения изображения', callback_data='sr')

kb.add(kb1, kb2, kb3, kb4, kb5, kb6, kb7)


# Initialize bot states
class BotStates(StatesGroup):
    class NTState(StatesGroup):
        style = State()
        content = State()

    wait = State()
    SRGANState = State()
    CYCLEGANState = State()


'''' Start handlers '''


# Handler to not upload image while current is processing
@dp.message_handler(commands=['start', 'help', 'Выбрать_категорию'], state=BotStates.wait)
async def on_message(message: types.Message):
    await bot.send_message(message.from_user.id, '<strong>Одновременно можено обрабатывать '
                                                 'только одно изображение.</strong>')


# Start/help handler
@dp.message_handler(commands=['start', 'help'], state='*')
async def on_message(message: types.Message):
    await bot.send_message(message.from_user.id,
                           f'Привет, {message.from_user.first_name}! Я-TSBot, умею трансформировать стиль картинки в '
                           f'один из возможных стилей и повышать разрешение изображения.🖼️\n\n '
                           'Попробуйте сами, для этого нажмите кнопку "<b>Выбрать_категорию</b>".',
                           reply_markup=kb_client)


# Choose one category of bot's functional
@dp.message_handler(commands=['Выбрать_категорию'], state='*')
async def handle_docs_photo(message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id,
                           '<i><b>Выберите одну из категорий.🔠</b></i>',
                           reply_markup=kb)


# Catch callback from previous handler
@dp.callback_query_handler()
async def style_choose_handler(query: types.CallbackQuery):
    global cur_style_set
    cur_style_set = query.data
    await bot.delete_message(chat_id=query.from_user.id, message_id=query.message.message_id)
    await query.message.answer(f'Выбрана категория <i><b>"{style_names[cur_style_set]}".</b></i>\nТеперь загрузите '
                               f'картинку/фото, стиль которой(-го) хотите изменить.\n\n '
                               '<i><b>⚠Будьте осторожны!⚠</b></i>\n Бот принимает на вход квадратное изображение(для '
                               f'переноса стиля) и максимальное разрешение {MAX_WIDTH_SR_INPUT}*{MAX_HEIGHT_SR_INPUT} '
                               f'на входе (для режима повышения разрешения изображения)')

    # Choose state of one bot's styles
    if cur_style_set == 'nt':
        await query.message.answer('1️⃣Шаг 1. Загрузите изображениe, <i><b>стиль которого будет переноситься.</b></i>')
        await BotStates.NTState.style.set()

    elif cur_style_set == 'sr':
        await BotStates.SRGANState.set()

    else:
        await BotStates.CYCLEGANState.set()


'''SRGAN processing handler'''


# Download and process image with SRGAN
@dp.message_handler(state=BotStates.SRGANState, content_types=['photo'])
async def download_process_SRGAN(message):
    photo_name = f'{message.from_user.id}_{cur_style_set}'

    # Check if image is not bigger than MAX_HEIGHT_SR_INPUT * MAX_WIDTH_SR_INPUT else send error message
    if message.photo[-1]['width'] * message.photo[-1]['height'] <= MAX_HEIGHT_SR_INPUT * MAX_WIDTH_SR_INPUT:

        # Download photo
        await message.photo[-1].download(
            destination_file=Path(f'ESRGAN/LR/{photo_name}.jpg'))
        await bot.send_message(message.from_user.id,
                               '⌛Пожалуйста, подождите. Изображение обрабатывается...⌛',
                               reply_markup=ReplyKeyboardRemove())

        # Set wait state to not upload other images while current is processing
        await BotStates.wait.set()

        # Process the image
        output_path = await asyncio.get_running_loop().run_in_executor(None, sr_processing, photo_name)

        # Go to main state of this handler
        await BotStates.SRGANState.set()

        # Send processed image
        await bot.send_photo(chat_id=message.from_user.id, photo=open(output_path, 'rb'),
                             caption=f'✅Pезультат повышения разрешения изображения', )
        print('SRGAN:Done...')
        await bot.send_message(chat_id=message.from_user.id,
                               text=f'Чтобы продолжить <b><i>в этом стиле</i></b>, загрузите следующее изображение.\
                                \n\nЧтобы <b><i>сменить стиль</i></b>, нажмите кнопку '
                                    f'<b><i>"/Выбрать_категорию".</i></b>',
                               reply_markup=kb_client)

        # Delete downloaded and processed images
        try:
            os.remove(f'ESRGAN/LR/{photo_name}.jpg')
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

        try:
            os.remove(f'ESRGAN/results/{photo_name}_rlt.png')
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

    else:
        await bot.send_message(message.from_user.id,
                               f"<strong>⚠Загрузите фото с разрешeнием не выше "
                               f"{MAX_WIDTH_SR_INPUT}*{MAX_HEIGHT_SR_INPUT}⚠</strong>")


'''CycleGAN processing handler'''


# Download and process image with CycleGAN
@dp.message_handler(state=BotStates.CYCLEGANState, content_types=['photo'])
async def download_process_CYCLEGAN(message):
    photo_name = f'{message.from_user.id}_{cur_style_set}'

    # Get name of chosen style
    kb_name = style_names[cur_style_set]

    # Download photo
    await message.photo[-1].download(
        destination_file=Path(f'photos/{photo_name}.jpg'))
    await bot.send_message(message.from_user.id,
                           '⌛Пожалуйста, подождите. Изображение обрабатывается...⌛', reply_markup=ReplyKeyboardRemove())

    # Set wait state to not upload other images while current is processing
    await BotStates.wait.set()

    # Process the image
    output_path = await asyncio.get_running_loop().run_in_executor(None, style_processing_cyclegan, photo_name)

    # Go to main state of this handler
    await BotStates.CYCLEGANState.set()

    # Send photo
    await bot.send_photo(chat_id=message.from_user.id, photo=open(output_path, 'rb'),
                         caption=f'✅Pезультат переноса стиля {kb_name}')
    print('CycleGAN:Done...')
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Чтобы продолжить <b><i>в этом стиле</i></b>, загрузите следующее изображение.\
                                \n\nЧтобы <b><i>сменить стиль</i></b>, нажмите кнопку '
                                f'<b><i>"/Выбрать_категорию".</i></b>',
                           reply_markup=kb_client)

    # Delete downloaded and processed images
    try:
        os.remove(f'photos/{photo_name}.jpg')
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))

    try:
        shutil.rmtree(f'photos/{style_dict[cur_style_set]}')
    except OSError as e:
        print("Error: %s - %s." % (e.filename, e.strerror))


''' Neural Transfer process handlers '''


# Download and process image with slow algorithm
@dp.message_handler(state=BotStates.NTState.style, content_types='photo')
async def download_style_photo(message):
    # Download style image
    await message.photo[-1].download(
        destination_file=Path(f'Neural_transfer/{message.from_user.id}_style.jpg'))
    await bot.send_message(message.from_user.id,
                           f'2️⃣Шаг 2.Загрузите изображениe <i><b>на которое будет переноситься стиль.</b></i>')

    # Set state for download and process content image
    await BotStates.NTState.next()


@dp.message_handler(state=BotStates.NTState.content, content_types='photo')
async def download_content_process_photo(message):
    # Download content image
    await message.photo[-1].download(
        destination_file=Path(f'Neural_transfer/{message.from_user.id}_content.jpg'))

    await bot.send_message(message.from_user.id,
                           '⌛Пожалуйста, подождите. Изображение обрабатывается...⌛', reply_markup=ReplyKeyboardRemove())

    # Set wait state to not upload other images while current is processing
    await BotStates.wait.set()

    # Process the images
    output_path = await asyncio.get_running_loop().run_in_executor(None, neural_transfer, message.from_user.id)

    # Go to main state of this handler
    await BotStates.NTState.content.set()

    await bot.send_photo(chat_id=message.from_user.id, photo=open(output_path, 'rb'),
                         caption=f'✅Pезультат переноса собственного стиля', )
    print('NT:Done...')
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Чтобы продолжить <b><i>в этом стиле</i></b>, загрузите следующее изображение.\
                                \n\nЧтобы <b><i>сменить стиль</i></b>, '
                                f'нажмите кнопку <b><i>"/Выбрать_категорию".</i></b>',
                           reply_markup=kb_client)

    # Delete downloaded and processed images
    for path_to_remove in [f'Neural_transfer/{message.from_user.id}_style.jpg',
                           f'Neural_transfer/{message.from_user.id}_content.jpg', output_path]:
        try:
            os.remove(path_to_remove)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))


''' Wrong file/command exception handlers '''


# Handler if user send photo as document. This need to avoid cases
# where file is too large and local server can drop while processing.
@dp.message_handler(content_types=['document'], state='*')
async def doc_handler(message: types.Message):
    await bot.send_message(message.from_user.id,
                           '😕Если это изображение, то отправьте его обычным способом.</strong>')


# Handler if user sent invalid commands or random words
@dp.message_handler(state='*')
async def cmd_not_found_handler(message: types.Message):
    await bot.send_message(message.from_user.id,
                           '😕Эта команда не поддерживаeтся на данный момент.')


# Handler if bot is just started and user wants to upload photo in no category.
@dp.message_handler(content_types=['photo'], state='*')
async def cat_not_found_handler(message: types.Message):
    await bot.send_message(message.from_user.id,
                           'Сначала выберите категорию.\nHажмите кнопку <i><b>"/Выбрать_категорию".</b></i>')


if __name__ == '__main__':
    print('Bot is working...')
    executor.start_polling(dp, skip_updates=True)
