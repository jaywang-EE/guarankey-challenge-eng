from flask import render_template, flash, redirect, url_for, Blueprint, request, session
from flask_login import current_user, login_required

from chatroom import models, db
from chatroom.utils import forms

from sqlalchemy import and_

import uuid 

import hashlib

chat = Blueprint('chat', __name__)

@chat.route('/chat/<int:rid>', methods=['GET', "POST"],endpoint='chat')
@login_required
def chatroom(rid):
    if request.method == 'GET':
        # set up session
        session['room'] = rid

        curr_room = db.session.query(models.Room).get(rid)
        # if room is deleted
        if not curr_room:
            return redirect(url_for('index'))
            
        room_user_obj = db.session.query(models.RoomUser).filter(and_(models.RoomUser.user_id == current_user.user_id, 
                                                                      models.RoomUser.room_uuid == curr_room.room_uuid)).first()

        if not room_user_obj: #if not in the room, register
            db.session.add(models.RoomUser(
                user_id=current_user.user_id, 
                room_uuid=curr_room.room_uuid
            ))
            db.session.commit()

        
        message_read_objs = db.session.query(models.MessageRead, models.Message).join(models.Message, models.MessageRead.message_id == models.Message.message_id).filter(and_(
            models.MessageRead.user_id == current_user.user_id,
            models.Message.room_id == rid
        )).all()
        init_message = ""
        for message_read_obj in message_read_objs:
            init_message += (message_read_obj.Message.message_content + '\n')
            db.session.delete(message_read_obj.MessageRead)
            db.session.commit()

        return render_template('chatroom.html', curr_room=curr_room, init_message=init_message)

@chat.route('/chat/create_room', methods=['GET', "POST"], endpoint='create')
@login_required
def create_room():
    if request.method == 'GET':
        return render_template('create_room.html')
    elif request.method == 'POST':
        form = forms.RoomCreateForm(formdata=request.form)
        if form.validate():
            db.session.add(models.Room(
                room_name=form.data['roomname'], 
                room_uuid=str(uuid.uuid4()), 
                room_owner_id=current_user.user_id
            ))
            db.session.commit()
            db.session.close()
            flash('創建房間: %s 成功'%(form.data['roomname']))
            return redirect(url_for('index'))
        else:
            for error in form.errors:
                flash(form.errors[error][0])
            return redirect(url_for('chat.create'))

@chat.route('/chat/delete_room/<int:rid>', methods=['GET', "POST"], endpoint='delete')
@login_required
def delete_room(rid):
    if request.method == 'GET':
        curr_room = db.session.query(models.Room).get(rid)
        return render_template('delete_room.html', curr_room=curr_room)
    elif request.method == 'POST':
        curr_room = db.session.query(models.Room).get(rid)
        print("DELETING ROOM: "+curr_room.room_name)
        
        db.session.delete(curr_room)
        db.session.commit()
        db.session.close()
        
        return redirect(url_for('index'))
