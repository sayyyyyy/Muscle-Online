from flask import request, Blueprint, jsonify
import hashlib
from flask_jwt_extended import create_access_token, unset_jwt_cookies

from models import db, User, User_Data

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/signup', methods=['GET', 'POST'])
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
            return {'code': 0, 'data': {'states': 'ユーザ作成に失敗しました'}}

        # User_Dataテーブルの追加
        new_user_data = User_Data(user_id=add_user.user_id)
        db.session.add(new_user_data)
        db.session.commit()
        
        access_token = create_access_token(add_user.user_id)
        add_user.token = access_token
        db.session.commit()

        return {'code': 1, 'data': {'states': 'ユーザ作成に成功しました', 'token': access_token}}
    else:
        return {'code': 0, 'data': {'states': '無効なHTTPメソッドです'}}


@user_bp.route('/signin', methods=['POST'])
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
        user.token = access_token
        db.session.commit()

        return {'code': 1, 'data': {'states': 'ログインに成功しました', 'token': access_token}}
    else:
        return {'code': 0, 'data': {'states': '無効なHTTPメソッドです'}}


@user_bp.route('/logout')
def logout():
    response = jsonify({'msg': 'logout success'})
    unset_jwt_cookies(response)
    return {'code': 1, 'data': {'states': 'ログアウトに成功しました'}}