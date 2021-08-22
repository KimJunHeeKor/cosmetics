import time

from flask_jwt_extended import *
from flask import Blueprint, jsonify, request

_fail_dict={
    'rt':'fail',
    'contents':'none',
    'pubDate':time.strftime('%Y-%M-%d %H:%m:%S')
    }

bp = Blueprint('log', __name__, url_prefix='/log')


## 회원 가입 API
@bp.route('/signup', methods=['POST'])
def sign_up():
    try:
        pass
    except Exception as err:
        print(f'[SIGNUP ERROR] : {err}')
        return jsonify(_fail_dict)

## 로그인 API
@bp.route('/login', methods=['POST'])
def login():
    try:
        #POST 확인
        if request.method != 'POST':
            return jsonify(_fail_dict)

        #POST parameters 확인
        user_id = request.form.get("user", type=str)
        password = request.form.get("password", type=str)

        #확인
        access_token = create_access_token(identity = user_id,
											expires_delta = False)
        user_info_dict = {'user': user_id, 'password':password, 'token':access_token}
        print(access_token)

        #TODO : User 정보를 DB에서 확인

        #TODO : JWT

        #TODO : login 정보를 DB에 기입

        json_dict={
            'rt': 'OK', 
            'contents':user_info_dict,
            'pubDate':time.strftime('%Y-%M-%d %H:%m:%S')
        }

        return jsonify(json_dict)
    except Exception as err:
        print(f'[LOGIN ERROR] : {err}')
        return jsonify(_fail_dict)


@bp.route('/test', methods=["GET"])
@jwt_required()
def user_only():
	cur_user = get_jwt_identity()
	if cur_user is None:
		return "User Only!"
	else:
		return "Hi!," + cur_user