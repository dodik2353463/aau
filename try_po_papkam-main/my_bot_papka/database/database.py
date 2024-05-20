from peewee import SqliteDatabase, Model, TextField, TimeField, AutoField


db = SqliteDatabase('sqlite_prazdnik.db')

class DB(Model):

    class Meta:
        database = db

class FileClass(DB):
    id = AutoField()
    user_id_tg = TextField(default=None, null=True)
    time = TimeField(null=True)

db.connect()
db.create_tables([FileClass], safe=True)
db.close()