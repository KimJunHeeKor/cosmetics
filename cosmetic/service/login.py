import time

from datetime import datetime, timedelta
from ..model.db_models import *
from flask_jwt_extended import *
from flask import Blueprint, json, jsonify, request
from .. import bcrypt

_fail_dict={
    'rt':'fail',
    'contents':'none',
    'pubDate':time.strftime('%Y-%M-%d %H:%m:%S')
    }

bp = Blueprint('log', __name__, url_prefix='/log')

def time_log():
    return time.strftime('%Y-%M-%d %H:%m:%S')
## 회원 가입 API
@bp.route('/signup', methods=['POST'])
def sign_up():
    try:
        #POST 전송 확인
        if request.method != 'POST':
            return jsonify(rt='fail')
        
        # POST parameters 확인
        acc_id = request.form.get("acc_id", type=str)
        password = request.form.get("password", type=str)
        name = request.form.get("name", type=str)
        created_date = datetime.now()

        password = bcrypt.generate_password_hash(password, 10)
        
        #sql을 db에 적용
        query = UserInfo(name=name, password=password, acc_id=acc_id, created_date=created_date)
        db.session.add(query)
        db.session.commit()

        return jsonify(rt='ok')

    except Exception as err:
        msg = f'[SIGNUP ERROR] [{time_log()}]: {err}'
        print(msg)
        return jsonify(_fail_dict)

## 로그인 API
@bp.route('/login', methods=['POST'])
def login():
    try:
        #POST 전송 확인
        if request.method != 'POST':
            return jsonify(_fail_dict), 400

        #POST parameters 확인
        acc_id = request.form.get("acc_id", type=str)
        password = request.form.get("password", type=str)

        #DB에 저장된 user 정보 일치 확인
        user_info = UserInfo.query.filter(UserInfo.acc_id == acc_id).all()
        hash_password = bcrypt.check_password_hash(user_info[0].password,password)
        if user_info is None or not hash_password:
            return jsonify(rt='fail'), 400

        #JWT 생성
        # access_token = create_access_token(identity = acc_id,
		# 									expires_delta = timedelta(minutes=10))
        #JWT 생성
        access_token = create_access_token(identity=acc_id, expires_delta=False)
        user_info[0].jwt=access_token
        db.session.commit()
        user_info_dict = {'accToken':access_token}

        #login 정보를 DB에 기입
        log_query = LogInfo(uid=user_info[0].id, login_time=datetime.now(), logout_time=datetime.now())
        db.session.add(log_query)
        db.session.commit()

        json_dict={
            'rt': 'OK', 
            'contents':user_info_dict,
            'pubDate':time.strftime('%Y-%M-%d %H:%m:%S')
        }

        return jsonify(json_dict)
    except Exception as err:
        msg = f'[LOGIN ERROR] [{time_log()}]: {err}'
        print(msg)
        return jsonify(_fail_dict)

@bp.route('/test', methods=['GET'])
@jwt_required()
def user_only():
    current_user = get_jwt_identity()
    #현재 접속한 유저가 DB에 저장된 유저인지 확인
    user_check = UserInfo.query.filter(UserInfo.acc_id == current_user).count()
    if user_check < 1:
        return jsonify(rt='fail')
    else:
        return jsonify(rt='ok')

@bp.route('/logout', methods=["GET"])
@jwt_required()
def logout():
    try:
        current_user = get_jwt_identity()
        user_info =  UserInfo.query.filter(UserInfo.acc_id==current_user).all()
        print(user_info[0].jwt)
        user_info[0].jwt = None
        print(user_info[0].jwt)
        db.session.commit()
        create_access_token(identity=current_user, expires_delta=timedelta(seconds=0))
    except Exception as err:
        msg = f'[LOGOUT ERRO] [{time_log()}] : {err}'
        print(msg)
        return jsonify(_fail_dict)
    return jsonify(rt='ok')