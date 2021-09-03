from datetime import datetime
import socket
import os
import json

from cosmetic.helper.methods import *
from cosmetic.helper.socket_connect import *
from cosmetic.lib.userskin_mths import analyzed_skin_status, average_user_skinvalue, median_users_skinvalue, max_user_skinvalue, min_user_skinvalue
from cosmetic.model.db_models import UserInfo



from flask import Blueprint, json, jsonify, request
from flask_jwt_extended import *

bp = Blueprint('userskin', __name__, url_prefix='/userskin')

# 로컬은 127.0.0.1의 ip로 접속한다.
HOST = '14.39.220.155'
# port는 위 서버에서 설정한 9999로 접속을 한다.
PORT= 34512

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


@bp.route("/values/history", methods=["GET"])
@jwt_required(fresh=True)
def search_user_skin_history():
    '''
    사용자에 대한 피부정보 측정 히스토리 전달 API
    '''
    try:
        acc_id = get_jwt_identity()
        user_history_date=[]
        
        user_history = calculate_user_skin_history(acc_id)
        
        for history in user_history:
            user_history_date.append(datetime.strftime(history.date, "%Y-%m-%d %H:%M:%S"))
        save_log("SEARCH USER SKIN HISTORY SUCCESS", f"({acc_id}) 사용자의 피부 히스토리를 불러왔습니다.")
        return jsonify(msg_dict("ok", {'history':user_history_date})), 200

    except Exception as err:
        save_log("SEARCH USER SKIN HISTORY ERROR", err, error=True)
        return jsonify(msg_dict('fail')), 400


@bp.route('/values/<compared_column>/<search_date>', methods=['GET'])
@jwt_required(fresh=True)
def seach_user_skin_values(compared_column, search_date):
    '''
    사용자에 대한 피부정보를 전달해주는 API
    '''
    try:
        if compared_column != "yearofbirth" and compared_column != "sex" \
            and compared_column!="residence" and compared_column!="nation"\
            and compared_column!="marriage" and compared_column!="job"\
            and compared_column!="education":
            return jsonify(msg_dict('fail')), 400

        #유저 id를 토큰으로 얻고 전달받은 시간정보를 설정된 datetime 형태로 변환
        acc_id = get_jwt_identity()
        search_datetime = convert_url_to_timeformat(search_date)

        # 해당 유저의 정보를 DB에서 찾는다.
        user = UserInfo.query.filter(UserInfo.acc_id == acc_id).first_or_404()
        if user is None:
            save_log("SEARCH USER SKIN VALUES ERROR", f"({acc_id})사용자를 검색하지 못했습니다.", error=True)
            return jsonify(msg_dict('fail')), 400
        
        
        #DB에서 값 받아오기
        analyzed_dict = calculate_user_skin_status(user, search_datetime)
        average_dict = calculate_average_user_skinvalue(compared_column,user, search_datetime)
        max_dict = calculate_max_user_skinvalue(compared_column,user, search_datetime)
        min_dict = calculate_min_user_skinvalue(compared_column,user, search_datetime)
        save_log("SEARCH USER SKIN VALUES SUCCESS", f"({acc_id})사용자의 피부상태, 평균값, 최대값, 최소값을 DB에서 가져왔습니다.")

        return jsonify(msg_dict('ok', {
                'anal': analyzed_dict,
                'avg': average_dict,
                'max': max_dict,
                'min': min_dict
            }))
    except Exception as err:
        save_log("SEARCH USER SKIN VALUES ERROR", err, error=True)
        return jsonify(msg_dict('fail')), 400


@bp.route('/survey-and-img', methods=['POST'])
@jwt_required(fresh=True)
def suervey():
    '''
    설문조사 결과를 받는 API
    '''
    try:
        # 소켓을 만든다.
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # connect함수로 접속을 한다.
        client_socket.connect((HOST, PORT))

        acc_id = get_jwt_identity()
        town = request.form.get('town')
        air_condition = request.form.get('air_condition')
        student_env = request.form.get('student_env')
        work_env = request.form.get('work_env')
        freel_env = request.form.get('freel_env')
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

        # 설문조사 정보를 dictionary로 저장
        socket_json = {
            "town" : town,
            "air_condition" : air_condition,
            "student_env" : student_env,
            "work_env" : work_env,
            "freel_env" : freel_env,
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
        
        #소켓통신 준비
        socket_json = json.dumps(socket_json)
        msg_mapping_list = [FULL_FACE, OIL_PAPER, SURVEY]
        
        # 디바이스 정보
        device_info = request.headers.get('User_Agent')

        # AI 서버와 소켓통신
        for msg in msg_mapping_list:

            send_msg_socket(msg, client_socket)

            if msg == FULL_FACE:
                # 아이디 정보 전달
                send_msg_socket(acc_id, client_socket)
                # 디바이스 정보 전달
                send_msg_socket(device_info, client_socket)
                # 전체 얼굴 이미지 전달
                send_img_socket(os.getcwd()+'/cosmetic/1.jpg', client_socket)

            elif msg == OIL_PAPER:
                # 기름종이 이미지 전달
                send_img_socket(os.getcwd()+'/cosmetic/2.jpg', client_socket)
                
            elif msg == SURVEY:
                # 설문조사 정보 전달
                send_msg_socket(socket_json, client_socket)

            # AI서버로 전송 결과 받기
            msg = rev_msg_socket(client_socket)
            if msg == '':
                print('no data')
                raise Exception
            
            # 로그 기록
            save_log("SURVEY SOCKET SUCCESS", f"({acc_id})"+msg)

        client_socket.close()
        return jsonify(msg_dict('ok'))

    except Exception as err:
        #로그 기록
        save_log("SURVEY ERROR", err, error=True)

        return jsonify(msg_dict('fail', "전송 실패"))