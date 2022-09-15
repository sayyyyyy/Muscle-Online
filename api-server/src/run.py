from flask import Flask, request
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, emit
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, create_access_token
from make_celery import make_celery
import time
import datetime

from models import db, User, Game, Room, User_Room, User_Data, Match
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
socketio = SocketIO(app, cors_allowed_origins="*")
celery = make_celery(app)

@celery.task()
def count_down(seconds):
    for second in range(1, seconds):
        time.sleep(1)
        print(seconds - second)

@app.route('/test', methods=['GET', 'POST'])
def aaa():

    if request.method == "POST":
        data = request.get_json()
        #video = camera.encode_decode(data["data"])
        camera.encode_decode(data['data'])
        #PoseDetection.get_frame(data['data'])
        
    else:
        print('get')
    return data

@socketio.on('join', namespace='/room')
def join(data):
    # ルームを作る側
    if 'room_token' in data:
        room_token = data['room_token']
        
        room = Room.query.filter_by(token=room_token, is_open=1).first()
        if not room:
            print('roomが見つかりません')
            return {'code': 0, 'data': {'states': 'roomが見つかりません'}}

        if not data['user_token']:
            print('user_Tokenが渡されていません')
            return {'code': 0, 'data': {'states': 'user_Tokenが渡されていません'}}
        
        user = User.query.filter_by(token=data['user_token']).first()
        if not user:
            print('ユーザが見つかりません')
            return {'code': 0, 'data': {'states': 'ユーザが見つかりません'}}

        add_user_room = User_Room(user_id=user.user_id, room_id=room.room_id)
        db.session.add(add_user_room)

        access_token = data['room_token']
        join_room(access_token)
    # ルームに入る側
    else:
        if not 'room_pass' in data:
            print('room_passが渡されていません')
            return {'code': 0, 'data': {'states': 'room_passが渡されていません'}}

        room_pass = data['room_pass']
        room = Room.query.filter_by(room_pass=room_pass, is_open=1).first()
        if not room:
            print('roomが見つかりません')
            return {'code': 0, 'data': {'states': 'roomが見つかりません'}}

        access_token = create_access_token(room.token)
        room.token = access_token
        room.is_open = 0
        db.session.commit()     
        join_room(access_token)

    user_room = User_Room.query.filter_by(room_id=room.room_id).all()
    user_list = {}
    for num, user in enumerate(user_room):
        user_data = User.query.filter_by(user_id=user.user_id).first()
        user_list[num] = {'name': user_data.name}

    emit('return', {'user_list': user_list, 'room_token': access_token}, to=access_token)
    return 0


@socketio.on('leave')
def leave_room(data):
    leave_room(data['room_token'])

@socketio.on('ready', namespace='/room')
def ready(data):
    # 2人とも準備完了ボタンを押されているか
    # modelsにisReadyカラムを追加してそれが0か1かで判定する

    if not 'user_token'in data:
        print('user_tokenが渡されていません')
        return 0

    user = User.query.filter_by(token=data['user_token']).first()
    user_isReady = User_Room.query.filter_by(user_id=user.user_id).first()
    user_isReady.isReady = not user_isReady.isReady
    db.session.commit()

    if user_isReady.isReady == 0:
        print('あなたが準備完了できていません')
        return 0

    
    if not 'room_token' in data:
        print('room_tokenが渡されていません')
        return 0

    room_token = data['room_token']
    room = Room.query.filter_by(token=room_token).first()

    if not room:
        print('ルームが見つかりません')
        return 0

    users_rooms = User_Room.query.filter_by(room_id=room.room_id).all()
    for user_room in users_rooms:
        if user_room.isReady == 0:
            print('相手が準備完了してません')
            return 0

    # 準備完了ボタンを押されてから10秒間残り秒数を返す
    count_down(10, room_token)
    
    # ゲーム開始
    start(30, room_token)
<<<<<<< HEAD
=======
    
    # (user_token, room_token, my_count, enemy_count, winner)
    # finish()
>>>>>>> develop
    

def start(limit, room_token):
    emit('start', {'data': 'ゲームスタート!'})
    print('ゲームを開始しました')

    count_down.delay(limit, room_token)

    # カウント機能を配置
    # func.delay()

def finish(user_token, room_token, my_count, enemy_count, winner):
    # User_Roomテーブルの更新 count
    user = User.query.filter_by(token=user_token).first()
    user_room = User_Room.query.filter_by(user_id=user.user_id).first()
    user_room.count = my_count

    # Matchテーブルの更新 winner_id is_finish, finish_time
    room = Room.query.filter_by(token=room_token).first()
    match = Match.query.filter_by(room_id=room.room_id).first()
    match.winner_id = winner
    match.is_finish = 1
    match.finish_time = datetime.datetime.now()

    # User_Dataテーブルの更新　全て
    # TODO: 引き分けの処理をどうするか
    user_data = User_Data.query.filter_by(user_id=user.user_id).first()
    if user.user_id == winner:
        user_data.num_of_win += 1
    else:
        user_data.num_of_lose += 1

    user_data.num_of_match += 1 


    db.session.commit()
    emit('finish', {'your_count': my_count, 'enemy_count': enemy_count, 'winner': winner})

    
@celery.task()
def count_down(seconds, room_token):
    for second in range(seconds):
        if second == seconds:
            break
        time.sleep(1)
        print(seconds - second)
        emit('count', {'count_down': seconds - second}, to=room_token)


if __name__ == '__main__':
    socketio.run(app, debug=True)
    # app.run()
