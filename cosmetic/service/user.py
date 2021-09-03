from datetime import datetime, timedelta

from cosmetic.helper.methods import time_log, msg_dict, save_log
from cosmetic.model.db_models import db, UserInfo, LogInfo

from flask_jwt_extended import *
from flask import Blueprint, jsonify, request
from cosmetic import bcrypt


## 전역변수 설정
# 블루프린트
bp = Blueprint('user', __name__, url_prefix='/user')
# 토큰 유지시간
acc_token_maintain_time=timedelta(minutes=10)
refresh_token_maintain_time = timedelta(minutes=30)


@bp.route('/signup', methods=['POST'])
def sign_up():
    '''
    회원 가입을 위한 API
    '''
    try:
        #POST 전송 확인
        if request.method != 'POST':
            save_log('SIGNUP ERROR','POST 전송이 아닙니다', error=True)
            return jsonify(msg_dict('fail','POST 전송이 아닙니다.')), 400
        
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

        if UserInfo.query.filter(UserInfo.acc_id == acc_id).count() > 0:
            save_log("SIGNUP ERROR", f"({acc_id})아이디가 존재합니다.",error=True)
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
        save_log("SIGNUP SUCCESS", f"({acc_id})아이디 생성 완료")

        return jsonify(msg_dict('ok')), 200

    except Exception as err:
        # 에러메시지 생성
        save_log("SIGNUP ERROR", err, error=True)

        return jsonify(msg_dict('fail', "아이디 생성 실패")), 400

@bp.route('/login', methods=['POST'])
def login():
    '''
    로그인 API
    '''
    try:
        #POST 전송 확인
        if request.method != 'POST':
            save_log("LOGIN ERROR", "POST 전송이 아닙니다.", error=True)
            return jsonify(msg_dict('fail','POST 전송이 아닙니다.')), 400

        #POST parameters 확인
        acc_id = request.form.get("acc_id", type=str)
        password = request.form.get("password", type=str)

        #DB에 저장된 user 정보 일치 확인
        user_info = UserInfo.query.filter(UserInfo.acc_id == acc_id).first()
        if user_info is None:
            save_log("LOGIN ERROR", f"({acc_id}) 없는 사용자입니다.", error=True)
            return jsonify(msg_dict('fail','없는 사용자입니다.')), 400

        hash_password = bcrypt.check_password_hash(user_info.password, password)
        if not hash_password:
            save_log("LOGIN ERROR", f"({acc_id}) 암호가 일치하지 않습니다.", error=True)
            return jsonify(msg_dict('fail', '암호가 일치하지 않습니다.')), 400

        #JWT 생성
        access_token = create_access_token(identity=acc_id, fresh=acc_token_maintain_time)
        refresh_token = create_refresh_token(identity=acc_id, expires_delta=refresh_token_maintain_time)
        user_info.jwt=refresh_token
        #JWT refresh token을 db에 저장(db 수정)
        db.session.commit()
        
        save_log("ACC,REF TOKEN SUCCESS", f"({acc_id}) 토큰 생성 및 DB에 저장 성공")

        user_info_dict = {'accToken':access_token, 'refToken':refresh_token}

        #login 정보를 DB에 기입
        log_query = LogInfo(uid=user_info.id, login_time=datetime.now(), logout_time=datetime.now())
        db.session.add(log_query)
        db.session.commit()
        save_log("LOGIN SUCCESS", f"({acc_id}) 접속 로그 DB에 저장, 로그인 성공")

        return jsonify(msg_dict('ok', user_info_dict))

    except Exception as err:
        # 에러메시지 생성
        save_log("LOGIN ERROR", err, error=True)

        return jsonify(msg_dict('fail'))

@bp.route('/test', methods=['GET'])
@jwt_required(fresh=True)
def user_only():
    '''
    API test
    '''
    current_user = get_jwt_identity()
    return jsonify(msg_dict('ok'))


@bp.route("/token/refresh", methods=["POST"])
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
        save_log("REF TOKEN ERROR", f"({acc_id}) DB에 없는 유저입니다.", error=True)
        #json 형태의 결과값 return
        return jsonify(msg_dict('fail', '없는 유저입니다.'))

    else: #성공시

        #토큰 재생성
        access_token = create_access_token(identity=current_user, fresh=acc_token_maintain_time)
        #로그 기록
        save_log("REF TOKEN SUCCESS", f"({acc_id}) refresh token 재발행")
        #json 형태의 결과값 return
        return jsonify(msg_dict('ok',{'access_token':access_token}))



@bp.route('/logout', methods=["POST"])
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


@bp.route('/userinfo/get', methods=["GET"])
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


@bp.route('/userinfo/update', methods=["PUT"])
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