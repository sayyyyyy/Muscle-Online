from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, emit
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token
from make_celery import make_celery
import time

from models import db, User, Game, Room, User_Room, User_Data
from app import app_bp
from user import user_bp
from room import room_bp
from history import history_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Blueprint設定
    app.register_blueprint(app_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(history_bp)
    
    return app

app = create_app()

# CORS設定
CORS(app)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

# 初期設定
db.init_app(app)
Migrate(app, db)


jwt = JWTManager(app)
socketio = SocketIO(app)
celery = make_celery(app)

@celery.task()
def count_down(seconds):
    for second in range(1, seconds):
        time.sleep(1)
        print(seconds - second)

@app.route('/test')
def aaa():
    count_down.delay(3)
    return 'a'

@socketio.on('join', namespace='/room')
def join(data):
    print(data)
    # ルームに入る側
    if data['room_token']:
        room_token = data['room_token']
        
        room = Room.query.filter_by(room_token=room_token, is_open=1).first()
        if not room:
            return {'code': 0, 'data': {'states': 'roomが見つかりません'}}

        if not data['user_token']:
            return {'code': 0, 'data': {'states': 'user_Tokenが渡されていません'}}
        
        user = User.query.filter_by(token=data['user_token']).first()
        if not user:
            return {'code': 0, 'data': {'states': 'ユーザが見つかりません'}}

        add_user_room = User_Room(user_id=user.user_id, room_id=room.room_id)
        db.session.add(add_user_room)

        access_token = create_access_token(room_pass)
        room.token = access_token
        room.is_open = 0
        db.session.commit()

        join_room(access_token)
    # ルームを作る側
    else:
        if data['room_pass']:
            return {'code': 0, 'data': {'states': 'room_passが渡されていません'}}

        room_pass = data['room_pass']
        room = Room.query.filter_by(room_pass=room_pass, is_open=1).first()
        if not room:
            return {'code': 0, 'data': {'states': 'roomが見つかりません'}}

        access_token = create_access_token(room_pass)
        room.token = access_token
        db.session.commit()     
        join_room(access_token)
    
    user_room = User_Room.query.filter_by(room_id=room.room_id).all()
    user_list = {}
    for num, user in enumerate(user_room):
        user_data = User.query.filter_by(user_id=user.user_id).first()
        user_list[num] = {'name': user_data.name}

    count_down.delay(4)
    emit('return', {'user_list': user_list, 'room_token': access_token})


@socketio.on('leave')
def leave_room(data):
    leave_room(data['room_token'])

@socketio.on('connect_s')
def connect(aa):
    print(aa)
    emit('return', {'aaa': 'aaa'})
    return "aa"

def send_message():
    pass
    
@celery.task()
def count_down(seconds):
    for second in range(1, seconds):
        time.sleep(1)
        print(seconds - second)
        emit('count', {'count_down': seconds - second})

if __name__ == '__main__':
    socketio.run(app, debug=True)
    # app.run()