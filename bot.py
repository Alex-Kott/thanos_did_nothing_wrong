import logging
from random import randint

from aiogram import Bot, Dispatcher
from aiogram.types import Message, ContentType
from aiogram.utils import executor
from aiohttp import BasicAuth
import requests

from config import BOT_TOKEN, PROXY_HOST, PROXY_PASS, PROXY_PORT, PROXY_USERNAME

# Configure logging
from models import Chat

logging.basicConfig(level=logging.INFO)

try:
    PROXY_AUTH = None
    PROXY_URL = None
    response = requests.get('https://api.telegram.org')
except Exception:
    PROXY_URL = f"socks5://{PROXY_HOST}:{PROXY_PORT}"
    PROXY_AUTH = BasicAuth(login=PROXY_USERNAME, password=PROXY_PASS)
bot = Bot(token=BOT_TOKEN, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
dp = Dispatcher(bot)


def init():
    Chat.create_table(fail_silently=True)


@dp.message_handler(commands=['ping'])
async def ping_handler(message: Message):
    await message.reply("I'm alive")


@dp.message_handler(commands=['crack'])
async def crack_handler(message: Message):
    print(message)

    chat = Chat.get(chat_id=message.chat.id)
    for i in range(1, chat.last_message_id):
        if randint(1, 2) == 2:
            print(i)
    # await bot.delete_message()


@dp.message_handler(content_types=[ContentType.TEXT])
async def text_handler(message: Message):

    print(message)

    chat = Chat.get_by_message(message)

    print(chat)
    # chat.last_message_id = message.message_id
    # chat.save()



if __name__ == "__main__":
    init()
    executor.start_polling(dp)
