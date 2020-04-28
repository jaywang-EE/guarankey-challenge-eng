from chatroom import db
from flask_login import UserMixin
# from chatroom import login_manager

class User(UserMixin, db.Model):
    __table__ = db.Model.metadata.tables['user_']
    def __repr__(self):
        return self.DISTRICT

    def get_id(self):
        return (self.user_id)

class Room(db.Model):
    __table__ = db.Model.metadata.tables['room']
    def __repr__(self):
        return self.DISTRICT

class RoomUser(db.Model):
    __table__ = db.Model.metadata.tables['room_user']
    def __repr__(self):
        return self.DISTRICT

class Message(db.Model):
    __table__ = db.Model.metadata.tables['message']
    def __repr__(self):
        return self.DISTRICT

class MessageRead(db.Model):
    __table__ = db.Model.metadata.tables['message_read']
    def __repr__(self):
        return self.DISTRICT

