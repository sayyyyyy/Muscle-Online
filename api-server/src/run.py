from flask import Flask, render_template, session, jsonify
from models import db, User, Game
from flask_migrate import Migrate
import flask_login
import initial_data
from flask_socketio import SocketIO, emit, join_room
from user import user_bp
from room import room_bp
import models
import time
import json

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # SQLAlchemy設定
    db.init_app(app)
    Migrate(app, db)
    

    return app


app = create_app()
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


app.register_blueprint(user_bp)
app.register_blueprint(room_bp)

socketio = SocketIO(app)

@app.route('/')
def test():
    return render_template('socket.html')



@app.route('/main')
@flask_login.login_required
def main_isLogin():
    user_room = models.User_Room.query.filter_by(room_id=7).all()
    print(type(user_room))
    print(user_room)
    return 'ログインしています'

@login_manager.unauthorized_handler
def main_isntLogin():
    return 'ログインしていません'

# @app.route('/<others>')
# def no_url(others):
#     print(others + 'というURLはありません。\n5秒後に遷移します')
#     time.sleep(5)
#     return redirect('/main')


@app.route('/show_')
def method_name():
    pass

@app.route('/add_data')
def add_data():
    initial_data.add_user()
    initial_data.add_gameformat()
    initial_data.add_game()
    initial_data.add_gameinfo(1, 1)
    initial_data.add_rankinginfo(1)

    game = Game().query.filter_by().first()
    print(game)
    print(game.name)
    print(game.description)
    return 'test'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# @socketio.on('connect', namespace='/room')
# def connect():
#     emit('join')

@socketio.on('join', namespace='/room')
@flask_login.login_required
def join(message):

    # ルームに入る側
    if message['room_pass']:
        room = models.Room.query.filter_by(room_pass=message['room_pass'], is_open=1).first()
        if not room:
            emit('return', {'code': 'error', 'state': 'Not exist Room'})
            return 0

        add_user_room = models.User_Room(user_id=flask_login.current_user.user_id, room_id=room.room_id)
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

        room = models.Room.query.filter_by(room_pass=session['room_pass'], is_open=1).first()
        if not room:
            emit('return', {'code': 'error', 'state': 'Not exist Room'})
            return 0        
        join_room(room.room_id)
    
    user_room = models.User_Room.query.filter_by(room_id=room.room_id).all()
    user_list = {}
    for num, user in enumerate(user_room):
        user_data = models.User.query.filter_by(user_id=user.user_id).first()
        user_list[num] = {'name': user_data.name}

    emit('return', {'user_list': user_list, 'room_pass': session['room_pass']})

@login_manager.unauthorized_handler
def not_login_join():
    emit('return', {'code': 'error', 'state': 'Not Login'})
    return 0


@socketio.on('leave')
def leave_room():
    leave_room(session['room_pass'])

def count_down(seconds):
    for second in range(1, seconds):
        time.sleeo(1)
        print(second)
        emit('count', {'count_down': second})

if __name__ == '__main__':
    socketio.run(app)
    # app.run()