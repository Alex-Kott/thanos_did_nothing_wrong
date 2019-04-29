from aiogram.types import Message, CallbackQuery
from peewee import SqliteDatabase, Model, IntegerField, TextField, DateTimeField, IntegrityError


class BaseClass(Model):
    class Meta:
        database = SqliteDatabase('db.sqlite3')


class Chat(BaseClass):
    name = TextField()
    last_message_id = IntegerField()
    last_crack = DateTimeField(null=True)

    @classmethod
    def get_by_message(cls, message: Message):
        try:
            chat, created = Chat.get_or_create(id=message.chat.id,
                                               name=message.chat.full_name,
                                               last_message_id=message.message_id)
        except IntegrityError:
            chat = Chat.get(id=message.chat.id)

        chat.last_message_id = message.message_id
        chat.save()

        return chat

    @classmethod
    def get_by_callback(cls, callback: CallbackQuery):

        return Chat.get(id=callback.message.chat.id)
