from flask import Flask, redirect, request, url_for
from models import db, User, Room, User_Room
from flask_migrate import Migrate
import flask_login
import hashlib
import time
import random, string

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
    create_room()
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

        email = 'test@a.a'
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

        email = 'test@a.a'
        password = 'password'

        user = User.query.filter_by(email=email, password=hashlib.sha256(password.encode('utf-8')).hexdigest()).first()

        if not user:
            return 'ユーザ名もしくはパスワードが異なります'
            # return redirect('/login')

        flask_login.login_user(user)

        return redirect('/main')
    else:
        email = 'test@a.a'
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

@app.route('/<others>')
def no_url(others):
    print(others + 'というURLはありません。\n5秒後に遷移します')
    time.sleep(5)
    return redirect('/main')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_room():
    room_pass = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(6))
    room_name = 'テスト部屋'
    
    room = Room(name=room_name)
    

    db.session.add(room)

    user_room = User_Room(user_id=user_id, room_id=room_id)
    db.session.add(user_room)
    db.session.commit()
    

if __name__ == '__main__':
    app.run()