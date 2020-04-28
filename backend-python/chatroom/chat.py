from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask_login import current_user, login_required

from chatroom import models, db

import hashlib

chat = Blueprint('chat', __name__)

@login_required
@chat.route('/chat', methods=['GET', "POST"],endpoint='chat')
def chatroom():
    if request.method == 'GET':
        return render_template('chatroom.html')