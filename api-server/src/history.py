from flask import Blueprint
import flask_login
import models

history_bp = Blueprint('hisrory_bp', __name__)

@history_bp.route('/history')
@flask_login.login_required
def history():
    user_data = models.User_Data.query.filter_by(user_id=flask_login.current_user.user_id).first()
    if not user_data:
        return {'code': 400, 'data': {'states': 'ユーザデータが見つかりません'}}
    
    return_data = {'match': user_data.num_of_match,
                    'win': user_data.num_of_win,
                    'lose': user_data.num_of_lose}

    # 一つ一つの試合結果 ゲーム情報と回数
    

    return {'code': 200, 'data': {'states': 'ユーザデータが見つかりました', 'user_data': return_data}}
