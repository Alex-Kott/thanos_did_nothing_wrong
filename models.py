from aiogram.types import Message
from peewee import SqliteDatabase, Model, IntegerField, TextField, DateTimeField


class BaseClass(Model):
    class Meta:
        database = SqliteDatabase('db.sqlite3')


class Chat(BaseClass):
    chat_id = IntegerField(primary_key=True)
    name = TextField()
    last_message_id = IntegerField()
    last_crack = DateTimeField(null=True)

    @classmethod
    def get_by_message(cls, message: Message):
        chat = Chat.get_or_create(chat_id=message.chat.id,
                                  name=message.chat.full_name,
                                  last_message_id=message.message_id)

