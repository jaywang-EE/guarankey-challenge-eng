from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from flask_socketio import SocketIO


db = SQLAlchemy()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    CSRFProtect(app)
    app.debug = True
    app.config.from_object('chatroom.settings.DebugConfig')
    db.init_app(app)
    with app.app_context():
        db.Model.metadata.reflect(db.engine)
    from chatroom.auth import auth
    app.register_blueprint(auth)
    from chatroom.chat import chat
    app.register_blueprint(chat)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    return app

