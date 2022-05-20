from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from make_celery import make_celery
import time

from models import db
from app import app_bp
from user import user_bp
from room import room_bp
from history import history_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # Blueprint設定
    app.register_blueprint(app_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(history_bp)
    
    return app

app = create_app()

# CORS設定
CORS(app)

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

# 初期設定
db.init_app(app)
Migrate(app, db)


jwt = JWTManager(app)
socketio = SocketIO(app)
celery = make_celery(app)

@celery.task()
def count_down(seconds):
    for second in range(1, seconds):
        time.sleep(1)
        print(seconds - second)

@app.route('/test')
def aaa():
    func = count_down.delay(3)
    func.wait()
    return 'a'

if __name__ == '__main__':
    socketio.run(app, debug=True)
    # app.run()