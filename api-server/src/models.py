from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_marshmallow import Marshmallow
from flask_login import UserMixin

db = SQLAlchemy()
ma = Marshmallow()

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    is_change_password = db.Column(db.Boolean, default=False)



    to_rooms = db.relationship('User_Room', backref='users', lazy=True)
    to_matches = db.relationship('Match', backref='users', lazy=True)
    to_user_data = db.relationship('User_Data', backref='users', lazy=True)
    to_rankings = db.relationship('Ranking', backref='users', lazy=True)

    def get_id(self):
        return (self.user_id)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'name', 'password', 'email', 'is_change_password')

class User_Room(db.Model):
    __tablename__ = 'users_rooms'

    user_room_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.room_id'), nullable=False)

class Room(db.Model):
    __tablename__ = 'rooms'

    room_id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(255), default="フレンド対戦")
    is_open = db.Column(db.Boolean, default=False)

    to_user_room = db.relationship('User_Room', backref='rooms', lazy=True)
    to_matchs = db.relationship('Match', backref='rooms', lazy=True)

class RoomSchema(ma.Schema):
    class Meta:
        fields = ('room_id', 'user1_id', 'user2_id', 'room_name', 'is_open', 'user')
    user = ma.Nested(UserSchema, many=False)

class Match(db.Model):
    __tablename__ = 'matches'

    match_id = db.Column(db.Integer, primary_key=True)
    game_info_id = db.Column(db.Integer, db.ForeignKey('gameinformations.game_info_id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.room_id'), nullable=False)
    user1_count = db.Column(db.Integer)
    user2_count = db.Column(db.Integer)
    winner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    is_finish = db.Column(db.Boolean, default=False)
    finish_time = db.Column(db.DateTime)

class User_Data(db.Model):
    __tablename__ = 'user_data'

    user_data_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    game_info_id = db.Column(db.Integer, db.ForeignKey('gameinformations.game_info_id'), nullable=False)
    num_of_match = db.Column(db.Integer, default=0)
    num_of_win = db.Column(db.Integer, default=0)
    num_of_lose = db.Column(db.Integer, default=0)

class GameInformation(db.Model):
    __tablename__ = 'gameinformations'

    game_info_id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'), nullable=False)
    game_format_id = db.Column(db.Integer, db.ForeignKey('gameformats.game_format_id'), nullable=False)
    game_rule = db.Column(db.String(255), default='HP')
    game_info = db.Column(db.Integer, nullable=False)

    to_match = db.relationship('Match', backref='gameinformations', lazy=True)
    to_user_data = db.relationship('User_Data', backref='gameinformations', lazy=True)

class GameFormat(db.Model):
    __tablename__ = 'gameformats'

    game_format_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    to_gameinfo = db.relationship('GameInformation', backref='gameformats', lazy=True)


class Game(db.Model):
    __tablename__ = 'games'

    game_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    to_gameinfo = db.relationship('GameInformation', backref='games', lazy=True)
    to_rankinginfo = db.relationship('RankingInformation', backref='games', lazy=True)

class RankingInformation(db.Model):
    __tablename__ = 'rankinginformations'

    ranking_info_id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    to_ranking = db.relationship('Ranking', backref='rankinginformations', lazy=True)


class Ranking(db.Model):
    __tablename__ = 'rankings'

    ranking_id = db.Column(db.Integer, primary_key=True)
    ranking_info_id = db.Column(db.Integer, db.ForeignKey('rankinginformations.ranking_info_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    rate = db.Column(db.Integer, nullable=False)
