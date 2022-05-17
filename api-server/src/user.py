from flask import request, redirect, url_for, Blueprint
from models import User, User_Data, db
import hashlib
import flask_login



user_bp = Blueprint('bupr', __name__)


@user_bp.route('/signup', methods=['GET', 'POST'])
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

        new_user_data = User_Data(user_id=add_user.user_id)
        db.session.add(new_user_data)
        db.session.commit()

        flask_login.login_user(new_user)

        return redirect('main')

@user_bp.route('/login', methods=['GET', 'POST'])
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

@user_bp.route('/logout')
def logout():
    flask_login.logout_user()
    return "ログアウトしました"