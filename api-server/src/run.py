from flask import Flask, redirect, request, url_for, session
from models import db, User, Room, User_Room, Match, Game
from flask_migrate import Migrate
import flask_login
import hashlib
import time
import random, string
import datetime
import initial_data

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

@app.route('/')
def test():
    return 'test'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        # email = request.form.get('email')
        # name = request.form.get('name')
        # password = request.form.get('password')

        email = 'test@a.a'
        name = 'test'
        password = 'password'

        user = User.query.filter_by(email=email).first()

        if user:
            return redirect(url_for('signup'))

        new_user = User(name=name, password=hashlib.sha256(password.encode('utf-8')).hexdigest(), email=email)
        
        db.session.add(new_user)
        db.session.commit()

        add_user = User.query.filter_by(email=email, password=hashlib.sha256(password.encode('utf-8')).hexdigest()).first()

        if not add_user:
            print('追加に失敗しました')
            return '追加に失敗しました'
            # return redirect('/signup')

        flask_login.login_user(new_user)


        return redirect(url_for('main'))
    else:

        # フロント側の処理が完成したらGETメソッドの処理は削除する

        email = 'test@a.b'
        name = 'test'
        password = 'password'

        user = User.query.filter_by(email=email).first()

        if user:
            print('そのメールアドレスは使われています')
            return 'そのメールアドレスは使われています'
            # return redirect('/signup')

        new_user = User(name=name, password=hashlib.sha256(password.encode('utf-8')).hexdigest(), email=email)
        
        db.session.add(new_user)
        db.session.commit()

        add_user = User.query.filter_by(email=email, password=hashlib.sha256(password.encode('utf-8')).hexdigest()).first()

        if not add_user:
            print('追加に失敗しました')
            return '追加に失敗しました'
            # return redirect('/signup')

        flask_login.login_user(new_user)

        return redirect('main')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        # email = request.form.get('email')
        # password = request.form.get('password')

        email = 'test@a.b'
        password = 'password'

        user = User.query.filter_by(email=email, password=hashlib.sha256(password.encode('utf-8')).hexdigest()).first()

        if not user:
            return 'ユーザ名もしくはパスワードが異なります'
            # return redirect('/login')

        flask_login.login_user(user)

        return redirect('/main')
    else:
        email = 'test@a.b'
        password = 'password'

        user = User.query.filter_by(email=email, password=hashlib.sha256(password.encode('utf-8')).hexdigest()).first()

        if not user:
            return 'ユーザ名もしくはパスワードが異なります'
            # return redirect('/login')

        flask_login.login_user(user)

        return redirect('/main')

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return "ログアウトしました"

@app.route('/main')
@flask_login.login_required
def main_isLogin():
    return 'ログインしています'

@login_manager.unauthorized_handler
def main_isntLogin():
    return 'ログインしていません'

# @app.route('/<others>')
# def no_url(others):
#     print(others + 'というURLはありません。\n5秒後に遷移します')
#     time.sleep(5)
#     return redirect('/main')

@app.route('/create_room')
@flask_login.login_required
def create_room():
    
    room_name = 'テスト部屋'

    while 1:
        room_pass = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(6))
        exist_room = Room(room_pass=room_pass, is_open=1).query.filter_by().first()
        if not exist_room:
            break

    room = Room(room_name=room_name, room_pass=room_pass, is_open=1)
    print(room)
    db.session.add(room)
    
    created_room = Room(room_pass=room_pass, is_open=1).query.filter_by().first()
    user_room = User_Room(user_id=flask_login.current_user.user_id, room_id=created_room.room_id)
    db.session.add(user_room)

    game_info_id = 1
    match = Match(game_info_id=game_info_id, room_id=created_room.room_id, finish_time=datetime.datetime.now())
    db.session.add(match)
    db.session.commit()

    session['room_pass'] = room_pass

    return session['room_pass']

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

if __name__ == '__main__':
    app.run()