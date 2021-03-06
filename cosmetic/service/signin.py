from datetime import datetime, timedelta

from cosmetic.helper.methods import msg_dict, save_log, update_db_logout
from cosmetic.model.db_models import db, UserInfo, LogInfo

from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from flask import Blueprint, jsonify, request, current_app
from cosmetic import bcrypt


## 전역변수 설정
# 블루프린트
bp = Blueprint('signin', __name__, url_prefix='/signin')

@bp.route('', methods=['POST'])
def signin():
    '''
    로그인 API
    '''
    try:
        #POST 전송 확인
        if request.method != 'POST':
            save_log.error("(LOGIN) POST 전송이 아닙니다.", error=True)
            return jsonify(msg_dict('fail','POST 전송이 아닙니다.')), 400

        #POST parameters 확인
        acc_id = request.form.get("acc_id", type=str)
        password = request.form.get("password", type=str)

        if acc_id == None or acc_id == "":
            save_log.error(f"(SIGNIN) acc_id 데이터가 없습니다.",error=True)
            return jsonify(msg_dict('fail',"acc_id 데이터가 없습니다.")), 400

        if password == None or password == "":
            save_log.error(f"(SIGNIN) password 데이터가 없습니다.",error=True)
            return jsonify(msg_dict('fail',"password 데이터가 없습니다.")), 400

        #DB에 저장된 user 정보 일치 확인
        user_info = UserInfo.query.filter(UserInfo.acc_id == acc_id).first()
        if user_info is None:
            save_log.error(f"(LOGIN) ({acc_id}) 없는 사용자입니다.", error=True)
            return jsonify(msg_dict('fail','없는 사용자입니다.')), 400

        hash_password = bcrypt.check_password_hash(user_info.password, password)
        if not hash_password:
            save_log.error( f"(LOGIN) ({acc_id}) 암호가 일치하지 않습니다.", error=True)
            return jsonify(msg_dict('fail', '암호가 일치하지 않습니다.')), 400

        #JWT 생성
        access_token = create_access_token(identity=acc_id, fresh=current_app.config["JWT_ACCESS_TOKEN_EXPIRES"])
        refresh_token = create_refresh_token(identity=acc_id, expires_delta=current_app.config["JWT_REFRESH_TOKEN_EXPIRES"])
        user_info.jwt=refresh_token
        #JWT refresh token을 db에 저장(db 수정)
        db.session.commit()
        
        save_log.info(f"(ACC,REF TOKEN SUCCESS)({acc_id}) 토큰 생성 및 DB에 저장 성공")

        user_info_dict = {'accToken':access_token, 'refToken':refresh_token}

        #login 정보를 DB에 기입
        log_query = LogInfo(uid=user_info.id, login_time=datetime.now(), logout_time=datetime.now()+current_app.config["JWT_ACCESS_TOKEN_EXPIRES"])
        db.session.add(log_query)
        db.session.commit()
        save_log.info(f"(LOGIN) ({acc_id}) 접속 로그 DB에 저장, 로그인 성공")

        return jsonify(msg_dict('ok', user_info_dict))

    except Exception as err:
        # 에러메시지 생성
        save_log.error(f"(LOGIN) {err}", error=True)

        return jsonify(msg_dict('fail'))


@bp.route("/token/refresh", methods=["GET"])
@jwt_required(refresh=True)
def refresh():
    '''
    access token 재발행 API
    '''
    acc_id = get_jwt_identity()

    #현재 접속한 유저가 DB에 저장된 유저인지 확인
    user_check = UserInfo.query.filter(UserInfo.acc_id == acc_id).first()
    if user_check is None: #실패시
        
        #로그 기록
        save_log.error(f"(REF TOKEN) ({acc_id}) DB에 없는 유저입니다.", error=True)
        #json 형태의 결과값 return
        return jsonify(msg_dict('fail', '없는 유저입니다.'))

    else: #성공시

        #토큰 재생성
        access_token = create_access_token(identity=acc_id, fresh=current_app.config["JWT_ACCESS_TOKEN_EXPIRES"])
        #로그 기록
        save_log.info(f"(REF TOKEN SUCCESS) ({acc_id}) refresh token 재발행")
        #DB 로그 갱신    
        update_db_logout(user_check, timedelta(hours=1))
        #json 형태의 결과값 return
        return jsonify(msg_dict('ok',{'access_token':access_token}))