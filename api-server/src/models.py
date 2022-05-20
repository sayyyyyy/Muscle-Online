from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_marshmallow import Marshmallow


db = SQLAlchemy()
ma = Marshmallow()

class User(db.Model):
    
    # テーブル名
    __tablename__ = 'users'

    # カラム
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    token = db.Column(db.String(511))
    is_change_password = db.Column(db.Boolean, default=False)


    # 外部キー制約
    to_matches = db.relationship('Match', backref='users', lazy=True)
    to_user_data = db.relationship('User_Data', backref='users', lazy=True)
    to_rankings = db.relationship('Ranking', backref='users', lazy=True)

    def get_id(self):
        return (self.user_id)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('user_id', 'name', 'password', 'email', 'is_change_password')


class Room(db.Model):
    __tablename__ = 'rooms'

    room_id = db.Column(db.Integer, primary_key=True)
    room_name = db.Column(db.String(255), default="フレンド対戦")
    room_pass = db.Column(db.String(6), nullable=False)
    token = db.Column(db.String(511))
    is_open = db.Column(db.Boolean, default=False)

    to_user_room = db.relationship('User_Room', backref='rooms', lazy=True)
    to_matchs = db.relationship('Match', backref='rooms', lazy=True)

class RoomSchema(ma.Schema):
    class Meta:
        fields = ('room_id', 'room_name', 'is_open')


class User_Room(db.Model):
    __tablename__ = 'users_rooms'

    user_room_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.room_id'), nullable=False)
    count = db.Column(db.Integer, default=0)

class User_RoomSchema(ma.Schema):
    class Meta:
        fields = ('user_room_id', 'user_id', 'room_id', 'user', 'room')
    user = ma.Nested(UserSchema, many=False)
    room = ma.Nested(RoomSchema, many=False)


class GameFormat(db.Model):
    __tablename__ = 'gameformats'

    game_format_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    to_gameinfo = db.relationship('GameInformation', backref='gameformats', lazy=True)

class GameFormatSchema(ma.Schema):
    class Meta:
        fields = ('game_format_id', 'name', 'description')


class Game(db.Model):
    __tablename__ = 'games'

    game_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    to_gameinfo = db.relationship('GameInformation', backref='games', lazy=True)
    to_rankinginfo = db.relationship('RankingInformation', backref='games', lazy=True)

class GameSchema(ma.Schema):
    class Meta:
        fields = ('game_id', 'name', 'description')


class GameInformation(db.Model):
    __tablename__ = 'gameinformations'

    game_info_id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'), nullable=False)
    game_format_id = db.Column(db.Integer, db.ForeignKey('gameformats.game_format_id'), nullable=False)
    game_rule = db.Column(db.String(255), default='HP')
    game_info = db.Column(db.Integer, nullable=False)

    to_match = db.relationship('Match', backref='gameinformations', lazy=True)

class GameInformationSchema(ma.Schema):
    class Meta:
        fields = ('game_info_id', 'game_id', 'game_format_id', 'game_rule', 'game_info', 'game', 'gameformat')
    game = ma.Nested(GameSchema, many=False)
    gameformat = ma.Nested(GameFormatSchema, many=False)



class Match(db.Model):
    __tablename__ = 'matches'

    match_id = db.Column(db.Integer, primary_key=True)
    game_info_id = db.Column(db.Integer, db.ForeignKey('gameinformations.game_info_id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.room_id'))
    winner_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    is_finish = db.Column(db.Boolean, default=False)
    finish_time = db.Column(db.DateTime)

class MatchSchema(ma.Schema):
    class Meta:
        fields = ('match_id', 'game_info_id', 'room_id', 'user1_count', 'user2_count', 'winner_id', 'is_finish', 'finish_time', 'gameinfo', 'room', 'user')
    game_info = ma.Nested(GameInformationSchema, many=False)
    room = ma.Nested(RoomSchema, many=False)
    user = ma.Nested(UserSchema, many=False)

class User_Data(db.Model):
    __tablename__ = 'user_data'

    user_data_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    num_of_match = db.Column(db.Integer, default=0)
    num_of_win = db.Column(db.Integer, default=0)
    num_of_lose = db.Column(db.Integer, default=0)

class User_DataSchema(ma.Schema):
    class Meta:
        fields = ('user_data_id', 'user_id', 'num_of_match', 'num_of_win', 'num_of_lose', 'user', 'gameinfo')
    user = ma.Nested(UserSchema, many=False)
    gameinfo = ma.Nested(GameInformationSchema, many=False)


class RankingInformation(db.Model):
    __tablename__ = 'rankinginformations'

    ranking_info_id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)

    to_ranking = db.relationship('Ranking', backref='rankinginformations', lazy=True)

class RankingInformationSchema(ma.Schema):
    class Meta:
        fields = ('ranking_info_id', 'game_id', 'name', 'description', 'game')
    game = ma.Nested(GameSchema, many=False)

class Ranking(db.Model):
    __tablename__ = 'rankings'

    ranking_id = db.Column(db.Integer, primary_key=True)
    ranking_info_id = db.Column(db.Integer, db.ForeignKey('rankinginformations.ranking_info_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    rate = db.Column(db.Integer, nullable=False)

class RankingSchema(ma.Schema):
    class Meta:
        fields = ('ranking_id', 'ranking_info_id', 'user_id', 'rate', 'rankinginfo', 'user')
    rankinginfo = ma.Nested(RankingInformationSchema, many=False)
    user = ma.Nested(UserSchema, many=False)