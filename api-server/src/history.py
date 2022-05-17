from flask import Blueprint
import flask_login
import models

history_bp = Blueprint('hisrory_bp', __name__)

@history_bp.route('/history')
@flask_login.login_required
def history():
    user_data = models.User_Data.query.filter_by(user_id=flask_login.current_user.user_id).first()
    if not user_data:
        return 'データが見つかりません'
    
    return_data = {'試合数': user_data.num_of_match,
                    '勝利数': user_data.num_of_win,
                    '敗北数': user_data.num_of_lose}

    # 一つ一つの試合結果 ゲーム情報と回数
    

    return {'code': 200, 'data': return_data}
