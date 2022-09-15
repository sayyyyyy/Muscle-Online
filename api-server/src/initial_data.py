import models
import hashlib

def add_user():

    email = 'test@a.a'
    name = 'test'
    password = 'password'

    user = models.User(name=name, password=hashlib.sha256(password.encode('utf-8')).hexdigest(), email=email)
    models.db.session.add(user)
    models.db.session.commit()

def add_gameformat():
    gameformat1 = models.GameFormat(name='ルームマッチ', description='ルームマッチ')
    gameformat2 = models.GameFormat(name='ランクマッチ', description='ランクマッチ')

    models.db.session.add(gameformat1)
    models.db.session.add(gameformat2)
    models.db.session.commit()

def add_game():
    game1 = models.Game(name='腹筋', description='腹筋')
    game2 = models.Game(name='腕立て伏せ', description='腕立て伏せ')

    models.db.session.add(game1)
    models.db.session.add(game2)
    models.db.session.commit()

def add_gameinfo(game_id, game_format_id):
    game_info1 = models.GameInformation(game_id=game_id, game_format_id=game_format_id, game_rule='HP', game_info=30)
    game_info2 = models.GameInformation(game_id=game_id, game_format_id=game_format_id, game_rule='HP', game_info=60)
    game_info3 = models.GameInformation(game_id=game_id, game_format_id=game_format_id, game_rule='Time', game_info=30)
    game_info4 = models.GameInformation(game_id=game_id, game_format_id=game_format_id, game_rule='Time', game_info=60)

    models.db.session.add(game_info1)
    models.db.session.add(game_info2)
    models.db.session.add(game_info3)
    models.db.session.add(game_info4)
    models.db.session.commit()

def add_rankinginfo(game_id):
    ranking_info = models.RankingInformation(game_id=game_id, name='テストランキング', description='テストランキングです')

    models.db.session.add(ranking_info)
    models.db.session.commit()