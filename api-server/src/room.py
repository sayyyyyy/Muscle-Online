from flask import Blueprint, session, request, redirect
import random
import string
from models import Room, db, User_Room, Match
import flask_login
import datetime

room_bp = Blueprint('room_bp', __name__)

@room_bp.route('/create_room')
@flask_login.login_required
def create_room():
    
    room_name = 'テスト部屋'

    while 1:
        room_pass = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(6))
        exist_room = Room.query.filter_by(room_pass=room_pass, is_open=1).first()
        if not exist_room:
            break

    room = Room(room_name=room_name, room_pass=room_pass, is_open=1)
    db.session.add(room)
    
    created_room = Room.query.filter_by(room_pass=room_pass, is_open=1).first()
    user_room = User_Room(user_id=flask_login.current_user.user_id, room_id=created_room.room_id)
    db.session.add(user_room)

    game_info_id = 1
    match = Match(game_info_id=game_info_id, room_id=created_room.room_id, winner_id=1, finish_time=datetime.datetime.now())
    db.session.add(match)
    db.session.commit()

    session['room_pass'] = room_pass

    return redirect('/')

@room_bp.route('/search_room', methods=['GET', 'POST'])
@flask_login.login_required
def search_room():
    if request.method == "POST":
        session['room_pass'] = ''
        room_pass = request.form.get('room_pass')

        search_room = Room.query.filter_by(room_pass=room_pass, is_open=1).first()
        if not search_room:
            print('ルームが見つかりませんでした')
            return 'ルームが見つかりませんでした'

        add_user_room = User_Room(user_id=flask_login.current_user.user_id, room_id=search_room.room_id)
        db.session.add(add_user_room)

        # isopenを0にする
        search_room.is_open = 0
        
        session['room_id'] = search_room.room_id

        db.session.commit()

        
        return 'POST'
    else:
        session['room_pass'] = ''
        room_pass = 'EzWY8K'

        search_room = Room.query.filter_by(room_pass=room_pass, is_open=1).first()
        if not search_room:
            print('ルームが見つかりませんでした')
            return 'ルームが見つかりませんでした'


        add_user_room = User_Room(user_id=flask_login.current_user.user_id, room_id=search_room.room_id)
        db.session.add(add_user_room)

        # isopenを0にする
        search_room.is_open = 0
        
        session['room_id'] = search_room.room_id
        
        db.session.commit()

        
        return 'a'