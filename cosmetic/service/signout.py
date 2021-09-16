from datetime import timedelta
from cosmetic.helper.methods import msg_dict, save_log, update_db_logout
from cosmetic.model.db_models import db, UserInfo

from flask_jwt_extended import *
from flask import Blueprint, jsonify


## 전역변수 설정
# 블루프린트
bp = Blueprint('signout', __name__, url_prefix='/signout')


@bp.route('', methods=["GET"])
@jwt_required(fresh=True)
def signout():
    '''
    로그아웃 API
    '''
    try:
        acc_id = get_jwt_identity()
        user_info =  UserInfo.query.filter(UserInfo.acc_id==acc_id).first()
        
        #JWT refresh token 초기화
        user_info.jwt = None
        # update_db_logout(user_info, timedelta(hours=0))
        db.session.commit()
        #로그 기록
        save_log.info(f"({acc_id})LOGOUT SUCCESS - Ref token 삭제 및 로그아웃 완료")
        
        return jsonify(msg_dict('ok'))

    except Exception as err:

        #로그 기록
        save_log.error("LOGOUT -"+ err, error=True)

        return jsonify(msg_dict('fail'))