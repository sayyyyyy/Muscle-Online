from run import socketio
import models
from flask_socketio import emit
from flask import session, join_room
import time

# @socketio.on('my event')
# def test_message(message):
#     emit('my response', {'data': message['data']})

# @socketio.on('my broadcast event')
# def test_message(message):
#     emit('my response', {'data': message['data']}, broadcast=True)

# @socketio.on('connect')
# def test_connect():
#     emit('my response', {'data': 'Connected'})

# @socketio.on('disconnect')
# def test_disconnect():
#     print('Client disconnected')


# @socketio.on('connect', namespace='/room')
# def start_room():
#     print('aaa')
#     emit('join', {})


# @socketio.on('join')
# def join_room(room_pass):
#     emit('stats', 'error')
#     # if not 'user_id' in session:
#     #     return 'ログインしてください'

#     # if not 'room_pass' in session:
#     #     return '操作をもう一度行ってください'

#     # # ルームに入る側
#     # if room_pass:
#     #     room = models.Rooom.query.filter_by(room_pass=room_pass, is_open=1).first()
#     #     if not room:
#     #         return 'そのようなルームパスはありません'

#     #     session['room_pass'] = room_pass
#     # # ルームを作る側
#     # else:
#     #     room = models.Room.query.filter_by(room_pass=session['room_pass'], is_open=1).first()
#     #     join_room(room.room_id)
    
#     # print('c')
#     # user_room = models.User.query.filter_by(room_id=room.room_id).all()
#     # print(user_room)

#     # emit('stats', {'user': user, 'room': room}, room=session['room_pass'])


# @socketio.on('leave')
# def leave_room():
#     leave_room(session['room_pass'])

# def count_down(seconds):
#     for second in range(1, seconds):
#         time.sleeo(1)
#         print(second)
#         emit('count', {'count_down': second})