import logging

from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.utils import executor

from config import BOT_TOKEN

# Configure logging
from models import Chat

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


def init():
    Chat.create_table(fail_silently=True)


@dp.message_handler(commands=['ping'])
async def ping_handler(message: Message):
    await message.reply("I'm alive")


@dp.message_handler(commands=['crack'])
async def crack_handler(message: Message):
    print(message)

    chat = Chat.get_or_create(chat_id=message.chat.id,
                              name=message.chat.full_name,
                              last_message_id=message.message_id)

    # await bot.delete_message()


if __name__ == "__main__":
    init()
    executor.start_polling(dp)
