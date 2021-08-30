import socket
import os

from ..helper.methods import time_log, msg_dict
from ..helper.socket_connect import *
from ..lib.userskin_mths import analyzed_skin_status, average_user_skinvalue, median_users_skinvalue, max_user_skinvalue, min_user_skinvalue
from ..model.db_models import Survey, UserInfo, Submit, db

from flask import Blueprint, json, jsonify, request
from flask_jwt_extended import *
from sqlalchemy import desc

bp = Blueprint('userskin', __name__, url_prefix='/userskin')

# 로컬은 127.0.0.1의 ip로 접속한다.
# HOST = 'localhost'
HOST = '14.39.220.155'
# port는 위 서버에서 설정한 9999로 접속을 한다.
PORT= 34512
# PORT=9999
# 소켓을 만든다.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect함수로 접속을 한다.
client_socket.connect((HOST, PORT))

@bp.route('/values', methods=['POST'])
def userskin_anal_status():
    '''
    피부분석 결과 전달 API
    '''
    if request.method != 'POST':
        return jsonify(msg_dict('fail', 'POST 전송이 아닙니다.'))

    analyzed_dict = analyzed_skin_status()
    average_dict = average_user_skinvalue()
    median_dict = median_users_skinvalue()
    max_dict = max_user_skinvalue()
    min_dict = min_user_skinvalue()

    return jsonify(msg_dict('ok', {
            'anal': analyzed_dict,
            'avg': average_dict,
            'med': median_dict,
            'max': max_dict,
            'min': min_dict
        }))


@bp.route('/survey-and-img', methods=['POST'])
@jwt_required(fresh=True)
def suervey():
    '''
    설문조사 결과를 받는 API
    '''
    try:
        acc_id = get_jwt_identity()
        user = UserInfo.query.filter(UserInfo.acc_id == acc_id).first()
        s_id = Submit.query.filter(Submit.uid == user.id).order_by(desc(Submit.id)).first()
        name = user.name
        year_of_birth = request.form.get('year_of_birth')
        marriage = request.form.get('marriage')
        childbirth = request.form.get('childbirth')
        job = request.form.get('job')
        student_env = request.form.get('student_env')
        work_env = request.form.get('work_env')
        freel_env = request.form.get('freel_env')
        education = request.form.get('education')
        hp_no = request.form.get('hp_no')
        email = request.form.get('email')
        env_Q1 = request.form.get('env_Q1')
        env_Q2 = request.form.get('env_Q2')
        env_Q3 = request.form.get('env_Q3')
        env_Q4 = request.form.get('env_Q4')
        life_Q1 = request.form.get('life_Q1')
        life_Q2 = request.form.get('life_Q2')
        life_Q3 = request.form.get('life_Q3')
        life_Q4 = request.form.get('life_Q4')
        life_Q5 = request.form.get('life_Q5')
        life_Q6 = request.form.get('life_Q6')
        life_Q7 = request.form.get('life_Q7')
        life_Q8 = request.form.get('life_Q8')
        life_Q9 = request.form.get('life_Q9')
        life_Q10 = request.form.get('life_Q10')
        dry_Q1 = request.form.get('dry_Q1')
        dry_Q2 = request.form.get('dry_Q2')
        dry_Q3 = request.form.get('dry_Q3')
        dry_Q4 = request.form.get('dry_Q4')
        dry_Q5 = request.form.get('dry_Q5')
        dry_Q6 = request.form.get('dry_Q6')
        sensitive_Q1 = request.form.get('sensitive_Q1')
        sensitive_Q2 = request.form.get('sensitive_Q2')
        sensitive_Q3 = request.form.get('sensitive_Q3')
        sensitive_Q4 = request.form.get('sensitive_Q4')
        sensitive_Q5 = request.form.get('sensitive_Q5')
        sensitive_Q6 = request.form.get('sensitive_Q6')
        sensitive_Q7 = request.form.get('sensitive_Q7')
        sensitive_Q8 = request.form.get('sensitive_Q8')
        sensitive_Q9 = request.form.get('sensitive_Q9')
        pigment_Q1 = request.form.get('pigment_Q1')
        pigment_Q2 = request.form.get('pigment_Q2')
        pigment_Q3 = request.form.get('pigment_Q3')
        pigment_Q4 = request.form.get('pigment_Q4')
        pigment_Q5 = request.form.get('pigment_Q5')
        pigment_Q6 = request.form.get('pigment_Q6')
        pigment_Q7 = request.form.get('pigment_Q7')
        wrinkle_Q1 = request.form.get('wrinkle_Q1')
        wrinkle_Q2 = request.form.get('wrinkle_Q2')
        wrinkle_Q3 = request.form.get('wrinkle_Q3')
        wrinkle_Q4 = request.form.get('wrinkle_Q4')
        wrinkle_Q5 = request.form.get('wrinkle_Q5')
        wrinkle_Q6 = request.form.get('wrinkle_Q6')
        wrinkle_Q7 = request.form.get('wrinkle_Q7')
        wrinkle_Q8 = request.form.get('wrinkle_Q8')
        wrinkle_Q9 = request.form.get('wrinkle_Q9')
        wrinkle_Q10 = request.form.get('wrinkle_Q10')
        wrinkle_Q11 = request.form.get('wrinkle_Q11')
        etc_Q1 = request.form.get('etc_Q1')
        etc_Q2 = request.form.get('etc_Q2')
        etc_Q3 = request.form.get('etc_Q3')
        etc_Q4 = request.form.get('etc_Q4')
        etc_Q5 = request.form.get('etc_Q5')
        etc_Q6 = request.form.get('etc_Q6')
        etc_Q7 = request.form.get('etc_Q7')
        etc_Q8 = request.form.get('etc_Q8')
        etc_Q9 = request.form.get('etc_Q9')
        etc_Q10 = request.form.get('etc_Q10')
        etc_Q11 = request.form.get('etc_Q11')
        etc_Q12 = request.form.get('etc_Q12')
        etc_Q13 = request.form.get('etc_Q13')
        etc_Q14 = request.form.get('etc_Q14')
        etc_Q15 = request.form.get('etc_Q15')
        etc_Q16 = request.form.get('etc_Q16')
        etc_Q17 = request.form.get('etc_Q17')
        # db.session.add(query)
        # db.session.commit()
        socket_json = {
            "acc_id" : acc_id,
            "user" : user,
            "s_id" : s_id,
            "name" : name,
            "year_of_birth" : year_of_birth,
            "marriage" : marriage,
            "childbirth" : childbirth,
            "job" : job,
            "student_env" : student_env,
            "work_env" : work_env,
            "freel_env" : freel_env,
            "education" : education,
            "hp_no" : hp_no,
            "email" : email,
            "env_Q1" : env_Q1,
            "env_Q2" : env_Q2,
            "env_Q3" : env_Q3,
            "env_Q4" : env_Q4,
            "life_Q1" : life_Q1,
            "life_Q2" : life_Q2,
            "life_Q3" : life_Q3,
            "life_Q4" : life_Q4,
            "life_Q5" : life_Q5,
            "life_Q6" : life_Q6,
            "life_Q7" : life_Q7,
            "life_Q8" : life_Q8,
            "life_Q9" : life_Q9,
            "life_Q10" : life_Q10,
            "dry_Q1" : dry_Q1,
            "dry_Q2" : dry_Q2,
            "dry_Q3" : dry_Q3,
            "dry_Q4" : dry_Q4,
            "dry_Q5" : dry_Q5,
            "dry_Q6" : dry_Q6,
            "sensitive_Q1" : sensitive_Q1,
            "sensitive_Q2" : sensitive_Q2,
            "sensitive_Q3" : sensitive_Q3,
            "sensitive_Q4" : sensitive_Q4,
            "sensitive_Q5" : sensitive_Q5,
            "sensitive_Q6" : sensitive_Q6,
            "sensitive_Q7" : sensitive_Q7,
            "sensitive_Q8" : sensitive_Q8,
            "sensitive_Q9" : sensitive_Q9,
            "pigment_Q1" : pigment_Q1,
            "pigment_Q2" : pigment_Q2,
            "pigment_Q3" : pigment_Q3,
            "pigment_Q4" : pigment_Q4,
            "pigment_Q5" : pigment_Q5,
            "pigment_Q6" : pigment_Q6,
            "pigment_Q7" : pigment_Q7,
            "wrinkle_Q1" : wrinkle_Q1,
            "wrinkle_Q2" : wrinkle_Q2,
            "wrinkle_Q3" : wrinkle_Q3,
            "wrinkle_Q4" : wrinkle_Q4,
            "wrinkle_Q5" : wrinkle_Q5,
            "wrinkle_Q6" : wrinkle_Q6,
            "wrinkle_Q7" : wrinkle_Q7,
            "wrinkle_Q8" : wrinkle_Q8,
            "wrinkle_Q9" : wrinkle_Q9,
            "wrinkle_Q10" : wrinkle_Q10,
            "wrinkle_Q11" : wrinkle_Q11,
            "etc_Q1" : etc_Q1,
            "etc_Q2" : etc_Q2,
            "etc_Q3" : etc_Q3,
            "etc_Q4" : etc_Q4,
            "etc_Q5" : etc_Q5,
            "etc_Q6" : etc_Q6,
            "etc_Q7" : etc_Q7,
            "etc_Q8" : etc_Q8,
            "etc_Q9" : etc_Q9,
            "etc_Q10" : etc_Q10,
            "etc_Q11" : etc_Q11,
            "etc_Q12" : etc_Q12,
            "etc_Q13" : etc_Q13,
            "etc_Q14" : etc_Q14,
            "etc_Q15" : etc_Q15,
            "etc_Q16" : etc_Q16,
            "etc_Q17" : etc_Q17
        }
        socket_json = str(socket_json)
        msg_mapping = MessageMapping()
        msg_mapping_list = [msg_mapping.FULL_FACE, msg_mapping.OIL_PAPER, msg_mapping.SURVEY]
        device_info = request.headers.get('User_Agent')

        for msg in msg_mapping_list:

            send_msg_socket(msg, client_socket)

            if msg == msg_mapping.FULL_FACE:
                send_msg_socket(acc_id, client_socket)
                send_msg_socket(device_info, client_socket)
                _, msg = send_img_socket(os.getcwd()+'/cosmetic/1.jpg', client_socket)
                print(msg)

            elif msg == msg_mapping.OIL_PAPER:
                _, msg = send_img_socket(os.getcwd()+'/cosmetic/2.jpg', client_socket)
                print(msg)
                
            elif msg == msg_mapping.SURVEY:
                msg = send_msg_socket(socket_json, client_socket)

            msg = rev_msg_socket(client_socket)
            if msg == '':
                print('no data')
                raise Exception
            # 데이터를 출력한다.
            log_msg = f"[RECEIVE SUCCESS] [{time_log()}]: {msg}"
            print('Received from : ', log_msg)

    except Exception as err:
        msg = f'[SURVEY ERROR] [{time_log()}] : {err}'
        print(msg)
        return jsonify(msg_dict('fail'))
    finally:
        client_socket.close()
        return jsonify(msg_dict('ok'))