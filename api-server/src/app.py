from flask import render_template, session, Response, request, Blueprint
import initial_data
from flask_socketio import emit, join_room
import time
import hashlib
from camera import VideoCamera
from flask_jwt_extended import create_access_token

from run import socketio
from models import db, User, Game, Room, User_Room, User_Data

app_bp = Blueprint('app_bp', __name__)


@app_bp.route('/')
def test():
    return render_template('socket.html')

@app_bp.route('/camera')
def index():
    return render_template('index.html')

    # "/" を呼び出したときには、indexが表示される。

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# returnではなくジェネレーターのyieldで逐次出力。
# Generatorとして働くためにgenとの関数名にしている
# Content-Type（送り返すファイルの種類として）multipart/x-mixed-replace を利用。
# HTTP応答によりサーバーが任意のタイミングで複数の文書を返し、紙芝居的にレンダリングを切り替えさせるもの。
#（※以下に解説参照あり）

@app_bp.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app_bp.route('/main')
def isLogin():
    if not 'user_token' in session:
        return {'code': 0, 'data': {'states': 'ログインしていません(user_tokenもない)'}}

    user = User.query.filter_by(token=session['user_token']).first()
    
    if not user:
        return {'code': 1, 'data': {'states': 'ログインしていません'}}
    
    return {'code': 1, 'data': {'states': 'ログインしています'}}



@app_bp.route('/add_data')
def add_data():
    initial_data.add_user()
    initial_data.add_gameformat()
    initial_data.add_game()
    initial_data.add_gameinfo(1, 1)
    initial_data.add_rankinginfo(1)

    game = Game().query.filter_by().first()
    return {'code': 1, 'data': {'states': 'データを追加しました'}}



def send_message():
    pass
    

def count_down(seconds):
    for second in range(1, seconds):
        time.sleep(1)
        print(second)
        emit('count', {'count_down': second})
