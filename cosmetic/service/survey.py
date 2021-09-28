import socket
import json

from cosmetic.helper.socket_connect import *
from cosmetic.helper.methods import *

# 로컬은 127.0.0.1의 ip로 접속한다.
HOST = '14.39.220.155'
# port는 위 서버에서 설정한 9999로 접속을 한다.
PORT= 34512

from flask import Blueprint, json, jsonify, request
from flask_jwt_extended import *

bp = Blueprint('survey', __name__, url_prefix='/survey')

@bp.route('', methods=['POST'])
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
        socket_json=dict(
            town = request.form.get('town'),
            air_condition = request.form.get('air_condition'),
            student_env = request.form.get('student_env'),
            work_env = request.form.get('work_env'),
            freel_env = request.form.get('freel_env'),
            env_Q1 = request.form.get('env_Q1'),
            env_Q2 = request.form.get('env_Q2'),
            env_Q3 = request.form.get('env_Q3'),
            env_Q4 = request.form.get('env_Q4'),
            life_Q1 = request.form.get('life_Q1'),
            life_Q2 = request.form.get('life_Q2'),
            life_Q3 = request.form.get('life_Q3'),
            life_Q4 = request.form.get('life_Q4'),
            life_Q5 = request.form.get('life_Q5'),
            life_Q6 = request.form.get('life_Q6'),
            life_Q7 = request.form.get('life_Q7'),
            life_Q8 = request.form.get('life_Q8'),
            life_Q9 = request.form.get('life_Q9'),
            life_Q10 = request.form.get('life_Q10'),
            dry_Q1 = request.form.get('dry_Q1'),
            dry_Q2 = request.form.get('dry_Q2'),
            dry_Q3 = request.form.get('dry_Q3'),
            dry_Q4 = request.form.get('dry_Q4'),
            dry_Q5 = request.form.get('dry_Q5'),
            dry_Q6 = request.form.get('dry_Q6'),
            sensitive_Q1 = request.form.get('sensitive_Q1'),
            sensitive_Q2 = request.form.get('sensitive_Q2'),
            sensitive_Q3 = request.form.get('sensitive_Q3'),
            sensitive_Q4 = request.form.get('sensitive_Q4'),
            sensitive_Q5 = request.form.get('sensitive_Q5'),
            sensitive_Q6 = request.form.get('sensitive_Q6'),
            sensitive_Q7 = request.form.get('sensitive_Q7'),
            sensitive_Q8 = request.form.get('sensitive_Q8'),
            sensitive_Q9 = request.form.get('sensitive_Q9'),
            pigment_Q1 = request.form.get('pigment_Q1'),
            pigment_Q2 = request.form.get('pigment_Q2'),
            pigment_Q3 = request.form.get('pigment_Q3'),
            pigment_Q4 = request.form.get('pigment_Q4'),
            pigment_Q5 = request.form.get('pigment_Q5'),
            pigment_Q6 = request.form.get('pigment_Q6'),
            pigment_Q7 = request.form.get('pigment_Q7'),
            wrinkle_Q1 = request.form.get('wrinkle_Q1'),
            wrinkle_Q2 = request.form.get('wrinkle_Q2'),
            wrinkle_Q3 = request.form.get('wrinkle_Q3'),
            wrinkle_Q4 = request.form.get('wrinkle_Q4'),
            wrinkle_Q5 = request.form.get('wrinkle_Q5'),
            wrinkle_Q6 = request.form.get('wrinkle_Q6'),
            wrinkle_Q7 = request.form.get('wrinkle_Q7'),
            wrinkle_Q8 = request.form.get('wrinkle_Q8'),
            wrinkle_Q9 = request.form.get('wrinkle_Q9'),
            wrinkle_Q10 = request.form.get('wrinkle_Q10'),
            wrinkle_Q11 = request.form.get('wrinkle_Q11'),
            etc_Q1 = request.form.get('etc_Q1'),
            etc_Q2 = request.form.get('etc_Q2'),
            etc_Q3 = request.form.get('etc_Q3'),
            etc_Q4 = request.form.get('etc_Q4'),
            etc_Q5 = request.form.get('etc_Q5'),
            etc_Q6 = request.form.get('etc_Q6'),
            etc_Q7 = request.form.get('etc_Q7'),
            etc_Q8 = request.form.get('etc_Q8'),
            etc_Q9 = request.form.get('etc_Q9'),
            etc_Q10 = request.form.get('etc_Q10'),
            etc_Q11 = request.form.get('etc_Q11'),
            etc_Q12 = request.form.get('etc_Q12'),
            etc_Q13 = request.form.get('etc_Q13'),
            etc_Q14 = request.form.get('etc_Q14'),
            etc_Q15 = request.form.get('etc_Q15'),
            etc_Q16 = request.form.get('etc_Q16'),
            etc_Q17 = request.form.get('etc_Q17')
        )

        s_id = find_or_create_subtmit(acc_id)

        #소켓통신 준비
        msg_mapping_list = []

        if request.files['fullface'].filename != '':
            msg_mapping_list.append('FULL_FACE')
        
        if request.files['oilpaper'].filename != '':
            msg_mapping_list.append('OIL_PAPER')

        come_data_complete = True

        # json 데이터의 value 존재 유무 확인
        for _, value in socket_json.items():
            if value is None or value == '':
                come_data_complete = False
                return jsonify(msg_dict(rt="fail", content="입력값을 확인하세요"))
                
        if come_data_complete:
            socket_json = json.dumps(socket_json)
            msg_mapping_list.append('SURVEY')

        # 디바이스 정보
        device_info = request.headers.get('User_Agent')
        
        # AI 서버와 소켓통신
        for msg in msg_mapping_list:
            #submit id 전송
            send_msg_socket(s_id, client_socket)
            #전송 데이터에 대한 메시지 전송
            send_msg_socket(msg, client_socket)

            if msg == FULL_FACE:
                # 아이디 정보 전달
                send_msg_socket(acc_id, client_socket)
                # 디바이스 정보 전달
                send_msg_socket(device_info, client_socket)
                # 전체 얼굴 이미지 전달
                send_img_socket(request.files["fullface"], client_socket)
                # send_img_socket(os.getcwd()+"\cosmetic\\1.jpg", client_socket)

            elif msg == OIL_PAPER:
                # 기름종이 이미지 전달
                send_img_socket(request.files['oilpaper'], client_socket)
                
            elif msg == SURVEY:
                # 설문조사 정보 전달
                send_msg_socket(socket_json, client_socket)

            # AI서버로 전송 결과 받기
            msg = rev_msg_socket(client_socket)
            if msg == '':
                print('no data')
                raise Exception
            
        # 로그 기록
        save_log.info(f"(SURVEY SOCKET SUCCESS) ({acc_id}) {msg}")

        client_socket.close()
        return jsonify(msg_dict('ok'))

    except Exception as err:
        #로그 기록
        save_log.error(f"(SURVEY) {err}", error=True)

        return jsonify(msg_dict('fail', "전송 실패"))