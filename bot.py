from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
from keyboards.client_keyboard import markup
from aiogram.types import ReplyKeyboardRemove
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher import filters
import conf 
from aiogram.dispatcher.middlewares import BaseMiddleware
from bd.bdnew import rec, showpassw
from loguru import logger
from aiogram.utils.executor import start_webhook

Dev_MODE = True

##------------------Блок ініціалізації-----------------##
API_Token = conf.TOKEN

ADMIN_ID = conf.ADMIN_ID
bot = Bot(token=API_Token)#os.getenv('TOKEN'))
storage = MemoryStorage()
dp = Dispatcher(bot, storage = storage)
logger.add("debug.txt")
# webhook settings
WEBHOOK_HOST = 'https://vmi957205.contaboserver.net'
WEBHOOK_PATH = '/prod_orxmstat'
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = '0.0.0.0'  # or ip 127.0.0.1
WEBAPP_PORT = 3004

##--------------Машини станів----------------------------##
class FSMzapPass(StatesGroup):
    about = State()
    login = State()
    pasw = State()

##---------------------Midelware-------------------------------##
class MidlWare(BaseMiddleware):
    async def on_process_update(self,update: types.Update,date: dict):
        logger.debug(update)
        logger.debug(update.message.from_user.id)
        if update.message.from_user.id not in ADMIN_ID:
            logger.debug(f"Хтось лівий зайшов {update.message.from_user.id}")
            raise CancelHandler()

##-------------------handlers--------------------------------------##
@dp.message_handler(commands=['start', 'help'],state= None)
async def send_welcome(message: types.Message):
    await message.reply("Вітаю! Щоб розпочати натисніть кнопку внизу!", reply_markup=markup)


##--------------------------новий пароль -----------------------##
@dp.message_handler(filters.Text(equals="Add new password 🔏"), state=None)
async def credet(message : types.Message):
    await FSMzapPass.about.set()
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    await message.answer("Опишіть до чого цей пароль:", reply_markup=ReplyKeyboardRemove())


@dp.message_handler(content_types=[types.ContentType.TEXT], state=FSMzapPass.about)
async def getcash(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['about'] = message.text
    await message.answer(f"Login: ")
    await FSMzapPass.next()


@dp.message_handler(content_types=[types.ContentType.TEXT], state=FSMzapPass.login)
async def getcash(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['login'] = message.text
    await message.answer(f"Pass: ")
    await FSMzapPass.next()


@dp.message_handler(content_types=[types.ContentType.TEXT], state=FSMzapPass.pasw)
async def description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['pass'] = message.text
    logger.debug(f"Опис - {message.text}")
    await rec(data['about'], data['login'], data['pass'])
    await message.answer(f"Пароль для {data['about']} внесено!", reply_markup=markup)
    await state.finish()


@dp.message_handler(filters.Text(equals="Show all passwords 📋"))
async def description(message: types.Message, state: FSMContext):
    await bot.send_chat_action(chat_id=message.from_user.id, action="typing")
    data = await showpassw()
    for i in data:
        str = f"{i[1]}\nLogin: {i[2]}\nPass: {i[3]}"
        await message.answer(str)


##----------------------------Різне----------------------##
@dp.message_handler()
async def echo(message: types.Message):
    if message.text == "Файл12":
        doc = open('debug.txt', 'rb')
        await message.reply_document(doc)
    elif message.text == "req":
        pass
    else:
        await message.answer("Не розумію", reply_markup=markup)
    
##-------------------Запуск бота-------------------------##
if Dev_MODE:
    print("Bot running")
    dp.middleware.setup(MidlWare())
    executor.start_polling(dp, skip_updates=True)
else:
    async def on_startup(dp):
        await bot.set_webhook(WEBHOOK_URL)
        logger.debug("Бот запущено")

    async def on_shutdown(dp):
        logger.debug('Зупиняюся...')
        await bot.delete_webhook()
        await dp.storage.close()
        await dp.storage.wait_closed()
    if __name__ == '__main__':
        dp.middleware.setup(MidlWare())
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )   
        