from flask import Flask, redirect, request, url_for, session
from models import db, User, Game
from flask_migrate import Migrate
import flask_login
import initial_data
from user import user_bp
from room import room_bp

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

@app.route('/')
def test():
    return 'test'



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

if __name__ == '__main__':
    app.run()