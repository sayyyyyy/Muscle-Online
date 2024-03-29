from flask import Blueprint, session, request, redirect
from flask_jwt_extended import create_access_token
import random
import string
from models import Room, db, User_Room, Match, User, GameInformation
import datetime

room_bp = Blueprint('room_bp', __name__)

@room_bp.route('/create_room', methods=['GET', 'POST'])
def create_room():
    if request.method == "POST":

        data = request.get_json()
        
        if not 'user_token' in data:
            return {'code': 0, 'data': {'states': 'tokenが渡されていません'}} 

        user = User.query.filter_by(token=data['user_token']).first()
        print(data)
        if not user:
            return {'code': 0, 'data': {'states': 'ユーザが見つかりませんでした'}} 


        if 'room_name' in data:
            room_name = data['room_name']
        else:
            room_name = 'テスト部屋'

        # room_passを取得
        while 1:
            room_pass = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(6))
            exist_room = Room.query.filter_by(room_pass=room_pass, is_open=1).first()
            if not exist_room:
                break

        # Roomテーブルの追加
        room = Room(room_name=room_name, room_pass=room_pass, is_open=1)
        db.session.add(room)
        db.session.commit()
        
        # User_Roomテーブルの追加
        created_room = Room.query.filter_by(room_pass=room_pass, is_open=1).first()
        user_room = User_Room(user_id=user.user_id, room_id=created_room.room_id)
        db.session.add(user_room)
        db.session.commit()

        # Matchテーブルの追加　一時的にgameinfoidを設定している
        game_info_id = 1
        match = Match(game_info_id=game_info_id, room_id=created_room.room_id, winner_id=1, finish_time=datetime.datetime.now())
        db.session.add(match)
        db.session.commit()

        access_token = create_access_token(room_pass)
        room.token = access_token
        db.session.commit()

        # ゲーム選択処理を追加した場合
        if 'game_id' in data and 'game_rule' in data:
            game = GameInformation.query.filter_by(game=data['game_id'], game_rule_id=data['game_rule'])
            # game.game_info_idをDBに追加する

        return {'code': 1, 'data': {'states': 'ルームを作成しました', 'room_token': access_token}}
    else:
        return {'code': 0, 'data': {'states': '無効なHTTPメソッドです'}}


@room_bp.route('/search_room', methods=['GET', 'POST'])
def search_room():
    if request.method == "POST":
        data = request.get_json()
        
        if not data['user_token']:
            return {'code': 0, 'data': {'states': 'tokenが渡されていません'}} 

        user = User.query.filter_by(token=data['user_token']).first()
        if not user:
            return {'code': 0, 'data': {'states': 'ユーザが見つかりませんでした'}} 

        if not data['room_pass']:
            return {'code': 0, 'data': {'states': 'room_passが入力されていません'}} 

        search_room = Room.query.filter_by(room_pass=data['room_pass'], is_open=1).first()
        if not search_room:
            return {'code': 0, 'data': {'states': 'ルームが見つかりませんでした'}}

        # User_Roomテーブルの追加
        add_user_room = User_Room(user_id=user.user_id, room_id=search_room.room_id)
        db.session.add(add_user_room)

        room_token = search_room.token

        db.session.commit()

        return {'code': 1, 'data': {'states': 'ルームが見つかりました', 'room_token': room_token}}
    else:
        return {'code': 0, 'data': {'states': '無効なHTTPメソッドです'}}