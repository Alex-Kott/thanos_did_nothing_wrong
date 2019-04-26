from peewee import SqliteDatabase, Model, IntegerField, TextField, DateTimeField


class BaseClass(Model):
    class Meta:
        database = SqliteDatabase('db.sqlite3')


class Chat(BaseClass):
    chat_id = IntegerField(primary_key=True)
    name = TextField()
    last_message_id = IntegerField()
    last_crack = DateTimeField(null=True)
