import flask
from flask_wtf.csrf import generate_csrf
from flask import render_template, session
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_login import current_user
from flask_sqlalchemy import SQLAlchemy

import uuid

from chatroom import create_app
from chatroom.request_hook import *

from chatroom.utils.sql import generate_connection

from sqlalchemy import and_

app = create_app()
#app.config['TESTING'] = False

# for chatroom

db = SQLAlchemy(app)#generate_connection()

"""
@app.route('/test')
def test():
    with db.cursor() as cur:
        cur.execute("SELECT col FROM test;")
        result, = cur.fetchone()
        return flask.jsonify({
            'result': result,
            'backend': 'python',
        })
"""
from chatroom import models

socketio = SocketIO(app, async_mode='eventlet')

@app.route('/')
def index():
    rids = None
    """
    with db.cursor() as cur:
        cur.execute("SELECT room_id, room_name FROM room;")
        rids = cur.fetchall()#[cols[0] for cols in cur.fetchall()]
        #print(rids)
    """
    rooms = db.session.query(models.Room).all()
    return render_template('index.html', rooms=rooms)


@socketio.on('connected')
def connected(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    print("connected")
    room_uuid = db.session.query(models.Room).get(room).room_uuid

    join_room(room)
    room_user_objs = db.session.query(models.RoomUser, models.User)\
        .join(models.User, models.RoomUser.user_id == models.User.user_id)\
        .filter(models.RoomUser.room_uuid == room_uuid).all()
    members = [room_user_obj.User.username for room_user_obj in room_user_objs]

    emit('user_change', {'members': members}, room=room)


@socketio.on('text')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    if message['msg']:
        msg = ' '+current_user.username + ': ' + message['msg']
        room = session.get('room')
        # insert_sql
        message_uuid = str(uuid.uuid4())
        message_obj = models.Message(
            user_id=current_user.user_id, 
            message_uuid=message_uuid, 
            message_content=msg,
            room_id=room,
        )
        db.session.add(message_obj)
        db.session.commit()

        db.session.refresh(message_obj)
        print(message_obj.message_id)

        # get all uses in this room
        room_uuid = db.session.query(models.Room).get(room).room_uuid
        room_user_objs = db.session.query(models.RoomUser).filter(models.RoomUser.room_uuid == room_uuid).all()
        for room_user_obj in room_user_objs:
            db.session.add(models.MessageRead(
                user_id=room_user_obj.user_id, 
                message_uuid=message_obj.message_uuid, 
                message_id=message_obj.message_id,
            ))

        db.session.commit()
        db.session.close()

        emit('message', {'msg': msg, 'uuid': message_uuid}, room=room)

@socketio.on('comfirm')
def comfirm(message):
    """Recieve comfirm message and delete the message_read"""
    #print("receive comfirm")
    if message['uuid']:
        message_read_obj = db.session.query(models.MessageRead).filter(and_(
            models.MessageRead.user_id == current_user.user_id,
            models.MessageRead.message_uuid == message['uuid']
        )).first()

        db.session.delete(message_read_obj)
        db.session.commit()
        print("MR:",db.session.query(models.MessageRead).count())
        db.session.close()

@socketio.on('left')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    room_uuid = db.session.query(models.Room).get(room).room_uuid

    room_user_obj = db.session.query(models.RoomUser).filter(and_(models.RoomUser.user_id == current_user.user_id, 
                                                                  models.RoomUser.room_uuid == room_uuid)).first()
    db.session.delete(room_user_obj)
    db.session.commit()

    print("OK")

    room_user_objs = db.session.query(models.RoomUser, models.User)\
        .join(models.User, models.RoomUser.user_id == models.User.user_id)\
        .filter(models.RoomUser.room_uuid == room_uuid).all()
    members = [room_user_obj.User.username for room_user_obj in room_user_objs]

    leave_room(room)
    emit('user_change', {'members': members}, room=room)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
    #app.run(debug=True)

