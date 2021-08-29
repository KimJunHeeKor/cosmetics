from ..helper.methods import save_error_log, time_log, msg_dict, save_log
from datetime import datetime, timedelta
from ..model.db_models import *
from flask_jwt_extended import *
from flask import Blueprint, json, jsonify, request
from .. import bcrypt


## 전역변수 설정
# 블루프린트
bp = Blueprint('log', __name__, url_prefix='/log')
# 토큰 유지시간
token_maintain_time=timedelta(minutes=5)


@bp.route('/signup', methods=['POST'])
def sign_up():
    '''
    회원 가입을 위한 API
    '''
    try:
        #POST 전송 확인
        if request.method != 'POST':
            msg = f'[SIGNUP ERROR] [{time_log()}]: ({request.remote_addr}) POST 전송이 아닙니다'
            save_error_log(msg)
            return jsonify(msg_dict('fail','POST 전송이 아닙니다.'))
        
        # POST parameters 확인
        acc_id = request.form.get("acc_id", type=str)
        password = request.form.get("password", type=str)
        name = request.form.get("name", type=str)
        created_date = datetime.now()

        if UserInfo.query.filter(UserInfo.acc_id == acc_id).count() > 0:
            msg = f'[SIGNUP ERROR] [{time_log()}]: ({request.remote_addr}) 아이디가 존재합니다.'
            save_log(msg)
            save_error_log(msg)
            return jsonify(msg_dict('fail',"아이디가 존재합니다."))
        #hashing password
        password = bcrypt.generate_password_hash(password, 10)
        
        #sql을 db에 적용(데이터 추가 작업)
        query = UserInfo(name=name, password=password, acc_id=acc_id, created_date=created_date)
        db.session.add(query)
        db.session.commit()
        msg = f'[SIGNUP] [{time_log()}]: ({request.remote_addr}) 아이디 생성 완료.'
        save_log(msg)

        return jsonify(msg_dict('ok')), 200

    except Exception as err:
        # 에러메시지 생성
        msg = f'[SIGNUP ERROR] [{time_log()}]: {err}'
        save_log(msg)
        save_error_log(msg)
        print(msg)
        return jsonify(msg_dict('fail')), 400

@bp.route('/login', methods=['POST'])
def login():
    '''
    로그인 API
    '''
    try:
        #POST 전송 확인
        if request.method != 'POST':
            return jsonify(msg_dict('fail', 'POST 전송이 아닙니다.')), 400

        #POST parameters 확인
        acc_id = request.form.get("acc_id", type=str)
        password = request.form.get("password", type=str)

        #DB에 저장된 user 정보 일치 확인
        user_info = UserInfo.query.filter(UserInfo.acc_id == acc_id).first()
        hash_password = bcrypt.check_password_hash(user_info.password,password)
        if user_info is None:
            return jsonify(msg_dict('fail','없는 사용자입니다.')), 400
        elif not hash_password:
            return jsonify(msg_dict('fail', 'mismatch password')), 400

        #JWT 생성
        access_token = create_access_token(identity=acc_id, fresh=token_maintain_time)
        refresh_token = create_refresh_token(identity=acc_id)
        user_info.jwt=refresh_token
        #JWT refresh token을 db에 저장(db 수정)
        db.session.commit()
        user_info_dict = {'accToken':access_token, 'refToken':refresh_token}

        #login 정보를 DB에 기입
        log_query = LogInfo(uid=user_info.id, login_time=datetime.now(), logout_time=datetime.now())
        db.session.add(log_query)
        db.session.commit()

        return jsonify(msg_dict('ok', user_info_dict))
    except Exception as err:
        msg = f'[LOGIN ERROR] [{time_log()}]: {err}'
        print(msg)
        return jsonify(msg_dict('fail'))

@bp.route('/test', methods=['GET'])
@jwt_required(fresh=True)
def user_only():
    '''
    API test
    '''
    current_user = get_jwt_identity()
    return jsonify(msg_dict('ok'))


@bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    '''
    access token 재발행 API
    '''
    current_user = get_jwt_identity()

    #현재 접속한 유저가 DB에 저장된 유저인지 확인
    user_check = UserInfo.query.filter(UserInfo.acc_id == current_user).first()
    if user_check is None:
        return jsonify(msg_dict('fail', '없는 유저입니다.'))
    else:
        access_token = create_access_token(identity=current_user, fresh=token_maintain_time)
        return jsonify(msg_dict('ok',{'access_token':access_token}))



@bp.route('/logout', methods=["POST"])
@jwt_required(fresh=True)
def logout():
    '''
    로그아웃 API
    '''
    try:
        current_user = get_jwt_identity()
        user_info =  UserInfo.query.filter(UserInfo.acc_id==current_user).first()
        
        #JWT refresh token 초기화
        user_info.jwt = None
        db.session.commit()
        
        return jsonify(msg_dict('ok'))

    except Exception as err:
        msg = f'[LOGOUT ERRO] [{time_log()}] : {err}'
        print(msg)
        return jsonify(msg_dict('fail'))