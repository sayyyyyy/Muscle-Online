from flask import Blueprint, request
import models

history_bp = Blueprint('hisrory_bp', __name__)

@history_bp.route('/history', methods=['GET', 'POST'])
def history():
    if request.method == "POST":
        user_data = request.get_json()

        if not user_data['user_token']:
            return {'code': 0, 'data': {'states': 'tokenが渡されていません'}}   
        user_data = models.User_Data.query.filter_by(token=user_data['user_token']).first()
        
        if not user_data:
            return {'code': 0, 'data': {'states': 'ユーザデータが見つかりません'}}
        
        return_data = {'match': user_data.num_of_match,
                        'win': user_data.num_of_win,
                        'lose': user_data.num_of_lose}

        # 一つ一つの試合結果 ゲーム情報と回数
        

        return {'code': 1, 'data': {'states': 'ユーザデータが見つかりました', 'user_data': return_data}}
    else:
        return {'code': 0, 'data': {'無効なHTTPメソッドです'}}