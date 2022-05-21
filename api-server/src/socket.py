from run import socketio, celery
from models import db, User, Game, Room, User_Room, User_Data

import time
from flask_jwt_extended import create_access_token, join_room, emit

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