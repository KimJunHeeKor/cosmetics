from datetime import datetime, timedelta

from cosmetic.helper.methods import msg_dict, save_log
from cosmetic.model.db_models import db, UserInfo, LogInfo

from flask_jwt_extended import *
from flask import Blueprint, jsonify


## 전역변수 설정
# 블루프린트
bp = Blueprint('signout', __name__, url_prefix='/signout')
# 토큰 유지시간
acc_token_maintain_time=timedelta(hours=1)
refresh_token_maintain_time = timedelta(days=1)



@bp.route('', methods=["GET"])
@jwt_required(fresh=True)
def logout():
    '''
    로그아웃 API
    '''
    try:
        acc_id = get_jwt_identity()
        user_info =  UserInfo.query.filter(UserInfo.acc_id==acc_id).first()
        
        #JWT refresh token 초기화
        user_info.jwt = None
        db.session.commit()
        #로그 기록
        save_log("LOGOUT SUCCESS", f"({acc_id})Ref token 삭제 및 로그아웃 완료")
        
        return jsonify(msg_dict('ok'))

    except Exception as err:

        #로그 기록
        save_log("LOGOUT ERROR", err, error=True)

        return jsonify(msg_dict('fail'))