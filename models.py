from datetime import datetime
from pony.orm import Database
from pony.orm.core import EntityMeta, Required, Optional, Set
from flask_login import UserMixin

db = Database()


class User(db.Entity, UserMixin):
    login = Required(str, unique=True)
    password = Required(str)
    first_name = Required(str)
    last_name = Optional(str)
    created_at = Required(datetime, default=datetime.utcnow)
    last_login = Optional(datetime)
    friends = Set('User', reverse='friends')
    sent = Set('Message', reverse='src')
    rcvd = Set('Message', reverse='dst')

    def check_password(self, password):
        return self.password == password

    def __str__(self):
        return ('%s %s' % (self.first_name, self.last_name)).rstrip()


class Message(db.Entity):
    src = Required(User, reverse='sent')
    dst = Optional(User, reverse='rcvd')
    text = Required(str)
    created_at = Required(datetime, default=datetime.utcnow)
    updated_at = Optional(datetime)
