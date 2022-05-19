from flask import Blueprint, request
import models

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
            room_list.qppend(room)

        if not room_list:
            return {'code': 0, 'data': {'states': '対戦履歴がありません1'}}        

        match_list = []
        for i in room_list:
            match = models.Match.query.filter_by(room_id = i.room_id)
            match_list.append(match)

        if not match_list:
            return {'code': 0, 'data': {'states': '対戦履歴がありません2'}}      

        return_data = {'match': user_data.num_of_match,
                        'win': user_data.num_of_win,
                        'lose': user_data.num_of_lose,
                        'user_room': user_room,
                        'room_list': room_list,
                        'match_list': match_list}

        # 一つ一つの試合結果 ゲーム情報と回数
        

        return {'code': 1, 'data': {'states': 'ユーザデータが見つかりました', 'user_data': return_data}}
    else:
        return {'code': 0, 'data': {'無効なHTTPメソッドです'}}