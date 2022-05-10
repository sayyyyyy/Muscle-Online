from flask import Flask, redirect
from models import db, User
from flask_migrate import Migrate
import hashlib

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    # SQLAlchemy設定
    db.init_app(app)
    Migrate(app, db)

    return app


app = create_app()

@app.route('/')
def test():
    return 'test'

if __name__ == '__main__':
    app.run()