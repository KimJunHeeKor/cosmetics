# 소켓을 사용하기 위해서는 socket을 import해야 한다.
import socket

from flask import request
from cosmetic.helper.methods import time_log
from typing import Tuple
# 로컬은 127.0.0.1의 ip로 접속한다.
HOST = 'localhost'
# HOST = '14.39.220.155'
# port는 위 서버에서 설정한 9999로 접속을 한다.
PORT = 9999
# PORT= 34512
# 소켓을 만든다.
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect함수로 접속을 한다.
client_socket.connect((HOST, PORT))




class MessageMapping():
    '''
    메시지 매핑 클래스 @20210825 KJH
    '''
    def __init__(self):
        self.FULL_FACE='FULL_FACE'
        self.OIL_PAPER='OIL_PAPER'
        self.SURVEY = 'SURVEY'

def rev_msg_socket(client_socket:socket) -> str:
    '''
    소켓통신으로 데이터 받는 메소드@20210830 KJH
    @param
    client_socket(socket) : 클라이언트 소켓
    @return
    msg(str) : 소켓통신으로 받은 메시지
    '''
    try:
        # server로 부터 전송받을 데이터 길이를 받는다.
        data = client_socket.recv(4)
        # 데이터 길이는 리틀 엔디언 형식으로 int를 변환한다.
        length = int.from_bytes(data, "little")
        # 데이터 길이를 받는다.
        data = client_socket.recv(length)
        if data == b'':
            print(f'[RECEIVE ERROR] : receive no data')
            return ''
        # 데이터를 수신한다.
        msg = data.decode()
        log_msg = f"[{time_log()}] [RECEIVE SUCCESS]: {msg}"
    except Exception as err:
        log_msg = f"[{time_log()}] [SOCKET ERROR]: {err}"
        msg = ''
    finally:
        print(log_msg)
        return msg

def send_msg_socket(msg:str, client_socket:socket):
    '''
    소켓통신을 통해 메시지 전달 메소드 @20210830 KJH
    @params
    msg(str): 전달 메시지
    client_socket(socket): 클라이언트 전송 소켓
    '''
    try:
        # 메시지 인코딩
        encode_msg = msg.encode()
        # 메시지 길이 전달
        encode_msg_len = len(encode_msg)
        client_socket.sendall(encode_msg_len.to_bytes(4, byteorder="little"))\
        # 해당 메시지 전달
        client_socket.sendall(encode_msg)
        log_msg = f'[{time_log()}] [MESSAGE SEND SUCCESS]'
    except Exception as err:
        log_msg = f'[{time_log()}] [MESSAGE SEND ERROR] : {err}'
    finally:
        print(log_msg)

def send_img_socket(load_file_path:str, client_socket:socket, buffer_size:int=1024) -> Tuple[bool, str]:
    '''
    # TODO : 이미지 파일을 불러 오는 것이 아닌 전송된 이미지로 변경해야함.
    소켓 통신으로 이미지를 서버로 전송하는 메소드 @20210825 KJH

    @params
    load_file_path(str) : 전송하는 이미지를 저장하는 경로
    client_socket(socket) : 클라이언트 소켓

    @return
    tuple(rt, msg)
        rt(bool) : 보낸결과
        msg(str) : 보낸결과 메시지
    '''
    try:
        # 보낼 파일 선언
        send_file = open(load_file_path, 'rb')
        # 이미지 데이터 정보가 변수
        image_data = send_file.read()
        # 이미지 데이터의 전체 길이
        length = len(image_data)
        # 이미지 데이터의 전체 길이를 보냄
        client_socket.sendall(length.to_bytes(4, byteorder="little"))
        # 이미지 데이터 정보가 담긴 변수를 초기화
        send_file.seek(0)
        # Buffer 사이즈 만큼 이미지 데이터를 전송
        image_data = send_file.read(buffer_size)
        # 이미지 데이터를 모두 보낼 때까지 데이터 전송
        while image_data:
            client_socket.send(image_data)
            image_data = send_file.read(buffer_size)
        msg = f'[{time_log()}] [IMAGE SEND SUCCESS]'
        rt = True
    except Exception as err:
        msg = f'[{time_log()}] [IMAGE SEND ERROR]: {err}'
        rt = False
    finally:
        send_file.close()
        return rt, msg

try:
    msg_mapping = MessageMapping()
    msg_mapping_list = [msg_mapping.FULL_FACE, msg_mapping.OIL_PAPER, msg_mapping.SURVEY]
    # device_info = request.headers.get('User_Agent')
    device_info = 'device'

    for msg in msg_mapping_list:

        send_msg_socket(msg, client_socket)

        if msg == msg_mapping.FULL_FACE:
            send_msg_socket('test_id', client_socket)
            send_msg_socket(device_info, client_socket)
            rt, msg = send_img_socket('1.jpg', client_socket)

        elif msg == msg_mapping.OIL_PAPER:
            rt, msg = send_img_socket('2.jpg', client_socket)

        elif msg == msg_mapping.SURVEY:
            send_msg_socket('hi', client_socket)

        msg = rev_msg_socket(client_socket)
        # 데이터를 출력한다.
        log_msg = f"[{time_log()}] [RECEIVE SUCCESS]: {msg}"
        print('Received from : ', log_msg)

except Exception as err:
    log_msg = f"[{time_log()}] [SOCKET ERROR]: {err}"
    print(log_msg)
finally:
    client_socket.close()