from flask import Blueprint, request, jsonify
import models
import json

history_bp = Blueprint('hisrory_bp', __name__)

@history_bp.route('/history', methods=['GET', 'POST'])
def history():
    if request.method == "POST":
        user_data = request.get_json()

        if not user_data['user_token']:
            return {'code': 0, 'data': {'states': 'tokenが渡されていません'}}  

        user = models.User.query.filter_by(token=user_data['user_token']).first()
        if not user:
             return {'code': 0, 'data': {'states': 'ユーザが見つかりません'}}

        user_data = models.User_Data.query.filter_by(user_id=user.user_id).first()
        if not user_data:
            return {'code': 0, 'data': {'states': 'ユーザデータが見つかりません'}}

        user_room = models.User_Room.query.filter_by(user_id=user.user_id).all()

        if not user_room:
            return {'code': 0, 'data': {'states': '対戦履歴がありません0'}}
        
        room_list = []
        for i in user_room:
            room = models.Room.query.filter_by(room_id = i.room_id).first()
            room_list.append(room.room_id)

        if not room_list:
            return {'code': 0, 'data': {'states': '対戦履歴がありません1'}}        

        match_winner_list = []
        match_gameinfo_list = []
        for i in room_list:
            match = models.Match.query.filter_by(room_id = i).first()
            if match.winner_id == user.user_id:
                match_winner_list.append('win')
            else:
                match_winner_list.append('lose')

            gameinfo = models.GameInformation.query.filter_by(game_info_id=match.game_info_id).first()
            match_gameinfo_list.append([gameinfo.game_format_id, gameinfo.game_rule])

        if not match_winner_list:
            return {'code': 0, 'data': {'states': '対戦履歴がありません2'}}



        return_data = {'match': user_data.num_of_match,
                        'win': user_data.num_of_win,
                        'lose': user_data.num_of_lose,
                        'match_history': {
                            'room_list': room_list,
                            'win_or_lose': match_winner_list,
                            'gameinfo': match_gameinfo_list
                        }
                        }

        # 直近50試合の試合結果(Match, winner) ゲーム情報(Match, gameinfo)と回数(User_Data, count)
        # まずルーム情報を持ってくる　そのroom_idを元にmatch, user_roomの値を取得
        

        return {'code': 1, 'data': {'states': 'ユーザデータが見つかりました', 'user_data': return_data}}
    else:
        return {'code': 0, 'data': {'states': '無効なHTTPメソッドです'}}
