from flask import Flask, render_template, session, jsonify, redirect, url_for, Response, request
from models import db, User, Game, Room, User_Room, User_Data
from flask_migrate import Migrate
import flask_login
import initial_data
from flask_socketio import SocketIO, emit, join_room
# from user import user_bp
from room import room_bp
from history import history_bp
import time
from flask_cors import CORS
import hashlib
from flask_jwt_extended import create_access_token,get_jwt,get_jwt_identity, \
                               unset_jwt_cookies, jwt_required, JWTManager
from camera import VideoCamera


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config.from_object('config.Config')
    CORS(app)
    # SQLAlchemy設定
    db.init_app(app)
    Migrate(app, db)
    

    return app


app = create_app()
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
jwt = JWTManager(app)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

# app.register_blueprint(user_bp)
app.register_blueprint(room_bp)
app.register_blueprint(history_bp)

socketio = SocketIO(app)
jwt = JWTManager(app)

@app.route('/')
def test():
    return render_template('socket.html')

@app.route('/camera')
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

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/main')
def isLogin():
    if not 'user_token' in session:
        return {'code': 0, 'data': {'states': 'ログインしていません(user_tokenもない)'}}

    user = User.query.filter_by(token=session['user_token']).first()
    
    if not user:
        return {'code': 1, 'data': {'states': 'ログインしていません'}}
    
    return {'code': 1, 'data': {'states': 'ログインしています'}}

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        user_data = request.get_json()

        # フロントからデータの受け取り
        if not user_data['user']['email']:
            return {'code': 0, 'data': {'states': 'emailが入力されていません'}}

        if not user_data['user']['name']:
            return {'code': 0, 'data': {'states': 'nameが入力されていません'}}

        if not user_data['user']['password']:
            return {'code': 0, 'data': {'states': 'passwordが入力されていません'}}

        email = user_data['user']['email']
        name = user_data['user']['name']
        password = user_data['user']['password']

        user = User.query.filter_by(email=email).first()
        if user:
            return {'code': 0, 'data': {'states': 'そのメールアドレスは既に使用されています'}}

        # データベースに保存
        new_user = User(name=name, password=hashlib.sha256(password.encode('utf-8')).hexdigest(), email=email)
        db.session.add(new_user)
        db.session.commit()

        # jwtでのログイン処理
        add_user = User.query.filter_by(email=email, password=hashlib.sha256(password.encode('utf-8')).hexdigest()).first()
        if not add_user:
            return {'data': {'states': 'ユーザ作成に失敗しました'}}

        new_user_data = User_Data(user_id=add_user.user_id)
        db.session.add(new_user_data)
        db.session.commit()
        
        access_token = create_access_token(add_user.user_id)
        add_user.token = access_token
        session['user_token'] = access_token
        db.session.commit()

        return {'code': 1, 'data': {'states': 'ユーザ作成に成功しました', 'token': access_token}}
    else:
        return {'code': 0, 'data': {'無効なHTTPメソッドです'}}


@app.route('/signin', methods=['POST'])
def signin():
    if request.method == "POST":
        # フロントからデータの受け取り
        user_data = request.get_json()

        if not user_data['user']['email']:
            return {'code': 0, 'data': {'states': 'emailが入力されていません'}}

        if not user_data['user']['password']:
            return {'code': 0, 'data': {'states': 'passwordが入力されていません'}}

        email = user_data['user']['email']
        password = user_data['user']['password']

        # パスワード等が違ったときの処理
        user = User.query.filter_by(email=email, password=hashlib.sha256(password.encode('utf-8')).hexdigest()).first()
        if not user:
            return {'code': 0, 'data': {'states': 'ユーザーが見つかりません'}}

        # jwtでのログイン処理
        access_token = create_access_token(user.user_id)
        session['user_token'] = access_token
        user.token = access_token
        db.session.commit()

        return {'code': 1, 'data': {'states': 'ログインに成功しました', 'token': access_token}}
    else:
        return {'code': 0, 'data': {'無効なHTTPメソッドです'}}

@app.route('/logout')
def logout():
    response = jsonify({'msg': 'logout success'})
    unset_jwt_cookies(response)
    return {'code': 1, 'data': {'states': 'ログアウトに成功しました'}}

@app.route('/add_data')
def add_data():
    initial_data.add_user()
    initial_data.add_gameformat()
    initial_data.add_game()
    initial_data.add_gameinfo(1, 1)
    initial_data.add_rankinginfo(1)

    game = Game().query.filter_by().first()
    return {'code': 1, 'data': {'states': 'データを追加しました'}}


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@socketio.on('join', namespace='/room')
@flask_login.login_required
def join(message):

    # ルームに入る側
    if message['room_pass']:
        room = Room.query.filter_by(room_pass=message['room_pass'], is_open=1).first()
        if not room:
            emit('return', {'code': 'error', 'state': 'Not exist Room'})
            return 0

        add_user_room = User_Room(user_id=flask_login.current_user.user_id, room_id=room.room_id)
        db.session.add(add_user_room)

        session['room_pass'] = message['room_pass']
        join_room(session['room_pass'])

        room.is_open = 0
        db.session.commit()
    # ルームを作る側
    else:
        if not 'room_pass' in session:
            emit('return', {'code': 'error', 'state': 'Not Room Pass'})
            return 0

        room = Room.query.filter_by(room_pass=session['room_pass'], is_open=1).first()
        if not room:
            emit('return', {'code': 'error', 'state': 'Not exist Room'})
            return 0        
        join_room(room.room_id)
    
    user_room = User_Room.query.filter_by(room_id=room.room_id).all()
    user_list = {}
    for num, user in enumerate(user_room):
        user_data = User.query.filter_by(user_id=user.user_id).first()
        user_list[num] = {'name': user_data.name}

    emit('return', {'user_list': user_list, 'room_pass': session['room_pass']})

# @login_manager.unauthorized_handler
# def not_login_join():
#     emit('return', {'code': 'error', 'state': 'Not Login'})
#     return 0


@socketio.on('leave')
def leave_room():
    leave_room(session['room_pass'])

def count_down(seconds):
    for second in range(1, seconds):
        time.sleep(1)
        print(second)
        emit('count', {'count_down': second})

if __name__ == '__main__':
    #socketio.run(app)
    app.run()