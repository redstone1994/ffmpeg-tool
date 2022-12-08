from flask import Flask, render_template
import sqlite3
from datetime import timedelta
from flask_socketio import SocketIO, emit
import ffmpeg

app = Flask(__name__, static_folder='static', template_folder='templates')

app.jinja_env.variable_start_string = '{['
app.jinja_env.variable_end_string = ']}'
# 自动重载模板文件
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = timedelta(seconds=1)
app.config['SECRET_KEY'] = 'secret_key'
socketio = SocketIO()
socketio.init_app(app, cors_allowed_origins='*')

name_space = '/dcenter'

@app.route('/index')
def index():  # put application's code here
    # conn = sqlite3.connect('ffmpeg.db')
    # c= conn.cursor()
    # c.execute("select * from ")
    message = "ddddddddddd"
    return render_template("index.html")


@app.route('/')
def index2():
    return render_template('index2.html')


@app.route('/push')
def push_once():
    event_name = 'dcenter'
    broadcasted_data = {'data': "test message!"}

    process1 = (
        ffmpeg
        .input("in_filename")
        .output('pipe:', format='rawvideo', pix_fmt='rgb24')
        .run_async(pipe_stdout=True)
    )

    socketio.emit(event_name, broadcasted_data, broadcast=False, namespace=name_space)
    return 'done!'


@socketio.on('connect', namespace=name_space)
def connected_msg():
    print('client connected.')


@socketio.on('disconnect', namespace=name_space)
def disconnect_msg():
    print('client disconnected.')


@socketio.on('my_event', namespace=name_space)
def mtest_message(message):
    print(message)
    emit('my_response',
         {'data': message['data'], 'count': 1})

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
