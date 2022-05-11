from flask import Flask, redirect, request, url_for
from models import db, User
from flask_migrate import Migrate
import flask_login
import hashlib

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

        add_user = User.query.filter_by(name=name, password=hashlib.sha256(password.encode('utf-8')).hexdigest()).first()

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

        add_user = User.query.filter_by(name=name, password=hashlib.sha256(password.encode('utf-8')).hexdigest()).first()

        if not add_user:
            print('追加に失敗しました')
            return '追加に失敗しました'
            # return redirect('/signup')

        flask_login.login_user(new_user)

        return redirect('main')

@app.route('/main')
@flask_login.login_required
def main_isLogin():
    return 'ログインしています'

@login_manager.unauthorized_handler
def main_isntLogin():
    return 'ログインしていません'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

if __name__ == '__main__':
    app.run()