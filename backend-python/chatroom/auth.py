from flask import render_template, flash, redirect, url_for, Blueprint, request
from flask_login import current_user, login_user, logout_user, login_required

from chatroom import models, db, login_manager
from chatroom.utils import forms

import hashlib

auth = Blueprint('auth', __name__)

#################################################################
# This project reference: https://zhuanlan.zhihu.com/p/66153415 #
#################################################################

# login manager required function
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(models.User).filter(models.User.user_id==user_id).first()

# login_requare 攔截後重定向
@login_manager.unauthorized_handler
def unauthorized():
    return redirect(url_for('auth.login'))

@auth.route('/logout', methods=['GET', "POST"],endpoint='logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['GET', "POST"],endpoint='login')
def login():
    if request.method == 'GET':
        print("LOGIN")
        if current_user.is_authenticated:
            print("OK")
            return redirect(url_for('index'))
        return render_template('login.html')
    elif request.method == 'POST':
        form = forms.LoginForm(formdata=request.form)
        if form.validate():
            password_hash = hashlib.md5(form.data['password'].encode('utf-8')).hexdigest()
            user_obj = db.session.query(models.User).filter(db.and_(models.User.username == form.data['username'],
                                                                models.User.password == password_hash)).first()
            if user_obj :
                login_user(user_obj)
                return redirect(url_for('index'))
            else:
                flash('用户名或密码错误')
                return redirect(url_for('auth.login'))
                pass
        else:
            for error in form.errors:
                flash(form.errors[error][0])
            return redirect(url_for('auth.login'))

@auth.route('/register', methods=['GET', "POST"],endpoint='register')
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        form = forms.RegisterForm(formdata=request.form)
        if form.validate():
            count = db.session.query(models.User).filter(models.User.username == form.data['username']).count()
            if count:
                flash('用户名已存在')
                return redirect(url_for('auth.register'))
            else:
                password_hash = hashlib.md5(form.data['password'].encode('utf-8')).hexdigest()
                db.session.add(models.User(username=form.data['username'],
                                           password=password_hash))
                db.session.commit()
                db.session.close()
                flash('注册成功')
                return redirect(url_for('auth.login'))
        else:
            for error in form.errors:
                flash(form.errors[error][0])
            return redirect(url_for('auth.register'))