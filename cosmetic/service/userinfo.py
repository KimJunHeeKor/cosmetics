from datetime import datetime, timedelta

from cosmetic.helper.methods import time_log, msg_dict, save_log
from cosmetic.model.db_models import db, UserInfo, LogInfo

from flask_jwt_extended import *
from flask import Blueprint, jsonify, request
from cosmetic import bcrypt


## 전역변수 설정
# 블루프린트
bp = Blueprint('userinfo', __name__, url_prefix='/userinfo')
# 토큰 유지시간
acc_token_maintain_time=timedelta(hours=1)
refresh_token_maintain_time = timedelta(days=1)


@bp.route('/get', methods=["GET"])
@jwt_required(fresh=True)
def userinfo():
    try:
        acc_id = get_jwt_identity()
        user_info =  UserInfo.query.filter(UserInfo.acc_id==acc_id).first()

        if user_info is None:
            save_log("GET USERINFO ERROR",f"({acc_id}) DB에 없는 유저입니다.", error=True)

            return jsonify(msg_dict('fail', '없는 유저입니다.'))

        user_info_json = jsonify(msg_dict('ok',{
            'name' : user_info.name,
            'year_of_birth' : user_info.year_of_birth,
            'marriage' : user_info.marriage,
            'childbirth' : user_info.childbirth,
            'job' : user_info.job,
            'education' : user_info.education,
            'hp_no' : user_info.hp_no,
            'email' : user_info.email,
            "sex" : user_info.sex,
            "residence" : user_info.residence,
            "nation" : user_info.nation
        }))
        save_log("GET USERINFO SUCCESS", f"({acc_id}) DB에서 유저 정보를 찾았습니다.")
        
        return user_info_json

    except Exception as err:

        save_log("GET USERINFO ERROR", err, error=True)

        return jsonify(msg_dict('fail'))


@bp.route('/update', methods=["PUT"])
@jwt_required(fresh=True)
def update():
    '''
    개인정보 수정
    '''
    try:
        acc_id = get_jwt_identity()
        user_info =  UserInfo.query.filter(UserInfo.acc_id==acc_id).first()

        name = request.form.get("name", type=str)
        password = request.form.get("password", type=str)
        year_of_birth = request.form.get("year_of_birth", type=str)
        marriage = request.form.get("marriage", type=str)
        childbirth = request.form.get("childbirth", type=str)
        job = request.form.get("job", type=str)
        education = request.form.get("education", type=str)
        hp_no = request.form.get("hp_no", type=str)
        email = request.form.get("email", type=str)
        sex = request.form.get("sex", type=str)
        residence = request.form.get("residence", type=str)
        nation = request.form.get("nation", type=str)

        user_info.name = name
        hash_password = bcrypt.check_password_hash(user_info.password, password)

        if hash_password:
            save_log("USER UPDATE ERROR", f"({acc_id})이전의 비밀번호와 동일합니다.", error=True)

            return jsonify(msg_dict('fail', '이전의 비밀번호와 동일합니다.')), 400

        user_info.password = password
        user_info.year_of_birth = year_of_birth
        user_info.marriage = marriage
        user_info.childbirth = childbirth
        user_info.job = job
        user_info.education = education
        user_info.hp_no = hp_no
        user_info.email = email
        user_info.sex = sex
        user_info.residence = residence
        user_info.nation = nation
        db.session.commit()
        #로그 저장
        save_log("USER UPDATE SUCCESS", f"({acc_id})유저 정보 수정 완료")

    except Exception as err:
        save_log("USER UPDATE ERROR", err, error=True)

        return jsonify(msg_dict('fail'))