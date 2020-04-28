import flask
import pymysql
import pymysql.cursors
from flask_wtf.csrf import generate_csrf
from flask import render_template
from flask_socketio import SocketIO

from chatroom import create_app
from chatroom.request_hook import *

app = create_app()

# for chatroom
socketio = SocketIO(app, async_mode='eventlet')

db = pymysql.connect(
    user='root',
    password='testpass',
    host='localhost',# 'db',

    database='challenge',
)

@app.route('/test')
def test():
    with db.cursor() as cur:
        cur.execute("SELECT col FROM test;")
        result, = cur.fetchone()
        return flask.jsonify({
            'result': result,
            'backend': 'python',
        })

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
    app.run(debug=True)

