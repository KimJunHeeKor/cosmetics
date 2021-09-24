from re import M
import smtplib
import random

from email.message import EmailMessage

from cosmetic.helper.methods import msg_dict, save_log
from cosmetic.model.db_models import db, UserInfo

from flask_jwt_extended import *
from flask import Blueprint, jsonify, request, current_app
from cosmetic import bcrypt



## 전역변수 설정
# 블루프린트
bp = Blueprint('userinfo', __name__, url_prefix='/userinfo')

@bp.route('/get', methods=["GET"])
@jwt_required(fresh=True)
def userinfo():
    try:
        acc_id = get_jwt_identity()
        user_info =  UserInfo.query.filter(UserInfo.acc_id==acc_id).first()

        if user_info is None:
            save_log.error(f"(GET USERINFO) ({acc_id}) DB에 없는 유저입니다.", error=True)

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
        save_log.info(f"(GET USERINFO SUCCESS) ({acc_id}) DB에서 유저 정보를 찾았습니다.")
        
        return user_info_json

    except Exception as err:

        save_log.error(f"(GET USERINFO) {err}", error=True)

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
            save_log.error(f"(USER UPDATE ERROR) ({acc_id})이전의 비밀번호와 동일합니다.", error=True)

            return jsonify(msg_dict('fail', '이전의 비밀번호와 동일합니다.')), 400
        
        user_info.password = bcrypt.generate_password_hash(password, 10)
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
        save_log.info(f"(USER UPDATE SUCCESS) ({acc_id}) 유저 정보 수정 완료")

        return jsonify(msg_dict('ok'))

    except Exception as err:
        save_log.error(f"(USER UPDATE ERROR) {err}", error=True)

        return jsonify(msg_dict('fail'))

@bp.route('/find/id', methods=["GET"])
def find_id():
    """
    id 찾기 위한 api
    """
    try:
        name = request.args.get("name")
        email = request.args.get("email")
        user_info = UserInfo.query.filter(UserInfo.name==name, UserInfo.email==email).first()
        acc_id = user_info.acc_id
        save_log.info(f"(FIND USER) {acc_id}")
        return jsonify(msg_dict("ok", {"id":acc_id}))

    except Exception as err:
        save_log.error(f"(FIND USER ERROR) {err}", error=True)

        return jsonify(msg_dict('fail'))

@bp.route("/send/newpassword", methods=["GET"])
def send_newpassword():
    """
    임의 암호 전달을 위한 API
    """

    EMAIL_ADDRESS = 'admin@ncyc.ai'
    EMAIL_PASSWORD = 'ysormxcqvcmdvgzi'
    SEND_EMAIL_LIST =[]
    PASSWORD_LENGTH = 8
    NEW_PASSWORD = ""

    try:
        acc_id = request.args.get("acc_id")
        user_info = UserInfo.query.filter(UserInfo.acc_id==acc_id).first()
        user_email = user_info.email

        # (PASSWORD_LENGTH)자리 임의의 암호 생성
        for i in range(PASSWORD_LENGTH):
            lower_rand_char =chr(random.randint(ord("a"), ord("z")))
            upper_rand_char = chr(random.randint(ord("A"), ord("Z")))
            rand_digit = str(random.randint(0, 9))
            rand = (lower_rand_char, upper_rand_char, rand_digit)[random.randint(0,2)]
            NEW_PASSWORD += rand

        # 패스워드 해쉬적용 및 DB 적용
        new_password = bcrypt.generate_password_hash(NEW_PASSWORD, 10)
        user_info.password = new_password
        db.session.commit()
        
        save_log.info(f"(PASSWORD CHANGED) ({acc_id}) 임의의 암호가 저장되었습니다.")

        
        # SEND_EMAIL_LIST.append(user_email)
        SEND_EMAIL_LIST.append(user_email)

        # 이메일 포멧 생성
        msg = EmailMessage()
        msg['Subject'] = "(Cosmetics) 비밀번호 변경"
        msg['From'] = EMAIL_ADDRESS 
        msg['To'] = SEND_EMAIL_LIST
        msg.set_content(
            '''
            <!DOCTYPE html>
            <html>
                <body>
                    <div style="display: flex; width: 800px; align-items: center;justify-content: center;align-content: center;flex-direction: column;">
                        <div style="width:100%;">
                            <p style="font-size: 30px; margin-bottom: 10px; color:rgb(109, 108, 108);"><strong style="color: black;">Cosmetics</strong>에서 알려드립니다.</p>
                            <p style="margin-top:10px; color: darkgrey;">365일 고객을 위해 최선을 다하겠습니다.</p>
                        </div>
                        
                        <div style="height: 100px; width:100%; background-color: rgba(129, 183, 230, 0.781); display:flex; justify-content: center; align-content: center; align-items: center; ">
                            <span><strong>{0}</strong>님의 임시 암호는 아래와 같습니다.</span>
                        </div>
                        <div style="width: 100%; display:flex; justify-content: center; align-content:center; align-items: center; border-top:3px solid rgb(183, 199, 214); border-bottom: 3px solid rgb(183, 199, 214);">
                            <h3 style="text-align: center;">임시비밀번호 : <span style="color: blue;">{1}</span></h3>
                        </div>
                        <div>
                            <p>임시 비밀번호를 사용해서 로그인 하신 후 바로 비밀번호를 변경하셔야 정상적으로 로그인이 가능합니다.<br>
                                다른 문의사항이 있으시면 고객센터로 문의해 주시기 바랍니다.
                                <br><br>
                                감사합니다.
                            </p>
                        </div>
                    </div>
                </body>
            </html>
            '''.format(acc_id,NEW_PASSWORD), subtype="html")

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD) 
            smtp.send_message(msg)
    
        save_log.info(f"(PASSWORD SENT TO EMAIL) ({acc_id}) 임의의 암호가 이메일({SEND_EMAIL_LIST})로 전송되었습니다.")

        return jsonify(msg_dict("ok", {"email": SEND_EMAIL_LIST}))

    except Exception as err:
        save_log.error(f"(PASSWORD CHANGED ERROR) {err}", error=True)
        return jsonify(msg_dict("fail"))