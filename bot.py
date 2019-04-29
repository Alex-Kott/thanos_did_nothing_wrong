import json
import logging
from asyncio import sleep
from datetime import datetime, timedelta

from random import randint

from aiogram import Bot, Dispatcher
from aiogram.types import Message, ContentType, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, \
    InputMediaAnimation, InputMediaPhoto
from aiogram.utils import executor
from aiogram.utils.exceptions import MessageToDeleteNotFound, MessageCantBeDeleted
from aiohttp import BasicAuth
import requests
from requests.exceptions import ConnectionError

from config import BOT_TOKEN, PROXY_HOST, PROXY_PASS, PROXY_PORT, PROXY_USERNAME
from models import Chat

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

file_handler = logging.FileHandler('info.log')
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)

try:
    PROXY_AUTH = None
    PROXY_URL = None
    response = requests.get('https://api.telegram.org')
except ConnectionError as e:
    PROXY_URL = f"socks5://{PROXY_HOST}:{PROXY_PORT}"
    PROXY_AUTH = BasicAuth(login=PROXY_USERNAME, password=PROXY_PASS)
bot = Bot(token=BOT_TOKEN, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
dp = Dispatcher(bot)


def init():
    Chat.create_table(fail_silently=True)


@dp.message_handler(commands=['ping'])
async def ping_handler(message: Message):
    await message.reply("I'm alive")


@dp.callback_query_handler()
async def callback_handler(callback: CallbackQuery):
    chat = Chat.get_by_callback(callback)
    chat.last_crack = datetime.now()
    chat.save()
    logger.info(callback)

    with open('./assets/glove/snap.gif', 'rb') as file:
        await bot.edit_message_media(chat_id=chat.id,
                                     message_id=callback.message.message_id,
                                     media=InputMediaAnimation(file))

    await sleep(2.9)
    with open('./assets/glove/glove180.png', 'rb') as file:
        await bot.edit_message_media(chat_id=chat.id,
                                     message_id=callback.message.message_id,
                                     media=InputMediaPhoto(file))

    await sleep(3)

    for i in range(chat.last_message_id, chat.last_message_id-100, -1):
        if randint(1, 2) == 2:
            await sleep(1)
            try:
                await bot.delete_message(chat_id=chat.id, message_id=i)
            except MessageToDeleteNotFound:
                pass
            except MessageCantBeDeleted:
                pass


@dp.message_handler(commands=['crack', 'snap'])
async def crack_handler(message: Message):
    chat = Chat.get_by_message(message)

    if chat.last_crack is None:
        pass
    elif chat.last_crack > (datetime.now() - timedelta(hours=8)):
        await message.reply("The time is not come yet")
        return

    keyboard = InlineKeyboardMarkup()

    callback_data = json.dumps({
        'data': 'tony stark will die'
    })
    button = InlineKeyboardButton('Snap', callback_data=callback_data)
    keyboard.row(button)
    with open('./assets/glove/glove180.png', 'rb') as file:
        await bot.send_photo(chat.id, file, reply_markup=keyboard)


@dp.message_handler(content_types=[ContentType.TEXT])
async def text_handler(message: Message):
    Chat.get_by_message(message)
    logger.info(message)


if __name__ == "__main__":
    init()
    executor.start_polling(dp)
