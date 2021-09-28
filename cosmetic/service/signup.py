from datetime import datetime

from cosmetic.helper.methods import msg_dict, save_log
from cosmetic.model.db_models import db, UserInfo

from flask import Blueprint, jsonify, request
from cosmetic import bcrypt

## 전역변수 설정
# 블루프린트
bp = Blueprint('signup', __name__, url_prefix='/signup')

@bp.route('', methods=['POST'])
def signup():
    '''
    회원 가입을 위한 API
    '''
    try:
        #POST 전송 확인
        if request.method != 'POST':
            save_log.error(f'(SIGNUP) POST 전송이 아닙니다', error=True)
            return jsonify(msg_dict('fail','POST 전송이 아닙니다.'))
            
        # POST parameters 확인
        acc_id = request.form.get("acc_id", type=str)
        password = request.form.get("password", type=str)
        name = request.form.get("name", type=str)
        year_of_birth = request.form.get("year_of_birth", type=int)
        marriage = request.form.get("marriage", type=str)
        childbirth = request.form.get("childbirth", type=str)
        job = request.form.get("job", type=str)
        education = request.form.get("education", type=str)
        hp_no = request.form.get("hp_no", type=str)
        email = request.form.get("email", type=str)
        sex = request.form.get("sex", type=str)
        residence = request.form.get("residence", type=str)
        nation = request.form.get("nation", type=str)
        created_date = datetime.now()
        
        if acc_id == None or acc_id == "":
            save_log.error(f"(SIGNUP) acc_id 데이터가 없습니다.",error=True)
            return jsonify(msg_dict('fail',"acc_id 데이터가 없습니다.")), 400

        if password == None or password == "":
            save_log.error(f"(SIGNUP) password 데이터가 없습니다.",error=True)
            return jsonify(msg_dict('fail',"password 데이터가 없습니다.")), 400

        if year_of_birth == None or year_of_birth == "":
            save_log.error(f"(SIGNUP) year_of_birth 데이터가 없습니다.",error=True)
            return jsonify(msg_dict('fail',"year_of_birth 데이터가 없습니다.")), 400

        if marriage == None or marriage == "":
            save_log.error(f"(SIGNUP) marriage 데이터가 없습니다.",error=True)
            return jsonify(msg_dict('fail',"marriage 데이터가 없습니다.")), 400

        if childbirth == None or childbirth == "":
            save_log.error(f"(SIGNUP) childbirth 데이터가 없습니다.",error=True)
            return jsonify(msg_dict('fail',"childbirth 데이터가 없습니다.")), 400

        if job == None or job == "":
            save_log.error(f"(SIGNUP) job 데이터가 없습니다.",error=True)
            return jsonify(msg_dict('fail',"job 데이터가 없습니다.")), 400

        if education == None or education == "":
            save_log.error(f"(SIGNUP) education 데이터가 없습니다.",error=True)
            return jsonify(msg_dict('fail',"education 데이터가 없습니다.")), 400

        if hp_no == None or hp_no == "":
            save_log.error(f"(SIGNUP) hp_no 데이터가 없습니다.",error=True)
            return jsonify(msg_dict('fail',"hp_no 데이터가 없습니다.")), 400

        if email == None or email == "":
            save_log.error(f"(SIGNUP) email 데이터가 없습니다.",error=True)
            return jsonify(msg_dict('fail',"email 데이터가 없습니다.")), 400

        if sex == None or sex == "":
            save_log.error(f"(SIGNUP) sex 데이터가 없습니다.",error=True)
            return jsonify(msg_dict('fail',"sex 데이터가 없습니다.")), 400

        if residence == None or residence == "":
            save_log.error(f"(SIGNUP) residence 데이터가 없습니다.",error=True)
            return jsonify(msg_dict('fail',"residence 데이터가 없습니다.")), 400

        if nation == None or nation == "":
            save_log.error(f"(SIGNUP) nation 데이터가 없습니다.",error=True)
            return jsonify(msg_dict('fail',"nation 데이터가 없습니다.")), 400

        if UserInfo.query.filter(UserInfo.acc_id == acc_id).count() > 0:
            save_log.error(f"(SIGNUP) ({acc_id})아이디가 존재합니다.",error=True)
            return jsonify(msg_dict('fail',"아이디가 존재합니다.")), 400

        #hashing password
        password = bcrypt.generate_password_hash(password, 10)
        
        #sql을 db에 적용(데이터 추가 작업)
        query = UserInfo(name=name, password=password,
                         acc_id=acc_id, created_date=created_date,
                         year_of_birth = year_of_birth,
                         marriage = marriage, childbirth = childbirth,
                         job = job, education = education,
                         hp_no = hp_no, email = email,
                         sex = sex, residence = residence,
                         nation = nation)
        db.session.add(query)
        db.session.commit()
        save_log.info(f"(SIGNUP SUCCESS) ({acc_id})아이디 생성 완료")

        return jsonify(msg_dict('ok')), 200

    except Exception as err:
        # 에러메시지 생성
        save_log.error(f"(SIGNUP) {err}", error=True)

        return jsonify(msg_dict('fail', "아이디 생성 실패")), 400