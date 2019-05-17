import json
import logging
from asyncio import sleep
from datetime import datetime, timedelta
from string import punctuation
from typing import List

from aiogram import Bot, Dispatcher
from aiogram.types import Message, ContentType, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, \
    InputMediaAnimation, InputMediaPhoto
from aiogram.utils import executor
from aiohttp import BasicAuth
import requests
from requests.exceptions import ConnectionError
from nltk.corpus import stopwords
from pymystem3 import Mystem

from config import BOT_TOKEN, PROXY_HOST, PROXY_PASS, PROXY_PORT, PROXY_USERNAME
from models import Chat, Ban

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
    Ban.create_table(fail_silently=True)
    Ban.get_or_create(id=1)


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


@dp.message_handler(commands=['crack', 'snap'])
async def crack_handler(message: Message):
    chat = Chat.get_by_message(message)

    if chat.last_crack is None:
        pass
    elif chat.last_crack > (datetime.now() - timedelta(hours=1)):
        await message.reply("The time has not come yet")
        return

    keyboard = InlineKeyboardMarkup()

    callback_data = json.dumps({
        'data': 'tony stark will die'
    })
    button = InlineKeyboardButton('Snap', callback_data=callback_data)
    keyboard.row(button)
    with open('./assets/glove/glove180.png', 'rb') as file:
        await bot.send_photo(chat.id, file, reply_markup=keyboard)


@dp.message_handler(commands=['spoiler'])
async def pin_spoiler(message: Message):
    if message.reply_to_message:
        await bot.pin_chat_message(chat_id=message.chat.id, message_id=message.reply_to_message.message_id)


def get_lemmatized_tokens(text: str) -> List[str]:
    mystem = Mystem()
    russian_stopwords = stopwords.words("russian")

    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if
              token not in russian_stopwords and token != " " and token.strip() not in punctuation]

    return tokens


async def ban_user(chat_id: int, user_id: int):
    ban = Ban.get(id=1)
    ban_expire_date = datetime.utcnow() + timedelta(minutes=ban.duration)
    await bot.restrict_chat_member(chat_id=chat_id, user_id=user_id,
                                   until_date=int(ban_expire_date.timestamp()),
                                   can_send_messages=False)
    ban.duration += 1
    ban.save()


async def squizduos_snova_naprosilsa(message: Message) -> None:
    if message.from_user.id == 57439615:
        lemmatized_tokens = get_lemmatized_tokens(message.text)
        if "напоминание" in set(lemmatized_tokens):
            await ban_user(message.chat.id, message.from_user.id)


async def irek_lose(message: Message) -> None:
    if message.from_user.id == 78911822:
        await message.reply('Ты сейчас проиграл')


@dp.message_handler(content_types=[ContentType.TEXT])
async def text_handler(message: Message):
    Chat.get_by_message(message)
    logger.info(message)

    await squizduos_snova_naprosilsa(message)
    await irek_lose(message)


if __name__ == "__main__":
    init()
    executor.start_polling(dp)
