from datetime import datetime
from pony.orm import Database
from pony.orm.core import Required, Optional, Set
from flask_login import UserMixin

db = Database()


class Timestampable:
    created_at = Required(datetime, default=datetime.utcnow)
    updated_at = Optional(datetime)


class User(db.Entity, UserMixin, Timestampable):
    login = Required(str, unique=True)
    password = Required(str)
    first_name = Required(str)
    last_name = Optional(str)
    last_login = Optional(datetime)
    messages = Set('Message')
    friends = Set('User')

    def check_password(self, password):
        return self.password == password


class Message(db.Entity, Timestampable):
    user = Required(User)
    text = Required(str)
