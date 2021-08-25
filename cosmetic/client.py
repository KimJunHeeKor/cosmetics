# 소켓을 사용하기 위해서는 socket을 import해야 한다.
import socket
from typing import Tuple
# 로컬은 127.0.0.1의 ip로 접속한다.
# HOST = 'localhost'
HOST = '14.39.220.155'
# port는 위 서버에서 설정한 9999로 접속을 한다.
# PORT = 9999
PORT= 34512
# 소켓을 만든다.
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket = socket.socket()
# connect함수로 접속을 한다.
client_socket.connect((HOST, PORT))

def img_send_socket(save_file_path:str, client_socket:socket, buffer_size:int=1024) -> Tuple[bool, str]:
    '''
    # TODO : 이미지 파일을 불러 오는 것이 아닌 전송된 이미지로 변경해야함.
    소켓 통신으로 이미지를 서버로 전송하는 메소드 @20210825 KJH

    @params
    save_file_path(str) : 전송하는 이미지를 저장하는 경로
    client_socket(socket) : 클라이언트 소켓

    @return
    tuple(rt, msg)
        rt(bool) : 저장결과
        msg(str) : 저장결과 메시지
    '''
    try:
        file = open(save_file_path, 'rb', encoding='utf8')
        image_data = file.read()
        length = len(image_data)
        client_socket.sendall(length.to_bytes(4, byteorder="little"))
        file.seek(0)
        image_data = file.read(buffer_size)
        while image_data:
            client_socket.send(image_data)
            image_data = file.read(buffer_size)
        msg = 'Image send success'
        rt = True
    except Exception as err:
        msg = f'[IMAGE SEND ERROR] : {err}'
        rt = False
    finally:
        file.close()
        return (rt, msg)


class MessageMapping():
    '''
    메시지 매핑 클래스 @20210825 KJH
    '''
    def __init__(self):
        self.FULL_FACE='FULL_FACE'
        self.OILY_PAPER='OILY_PAPER'

try:
    msg_mapping = MessageMapping()
    msg_mapping_list = [msg_mapping.FULL_FACE, msg_mapping.OILY_PAPER]
    for msg in msg_mapping_list:
        msg = msg
        # 메시지를 바이너리(byte)형식으로 변환한다.
        data = msg.encode()
        # 메시지 길이를 구한다.
        length = len(data)
        # # server로 리틀 엔디언 형식으로 데이터 길이를 전송한다.
        client_socket.sendall(length.to_bytes(4, byteorder="little"))
        # 데이터를 전송한다.
        client_socket.sendall(data)

        if msg == msg_mapping.FULL_FACE:
            img_send_socket('1.jpg', client_socket)
        elif msg == msg_mapping.OILY_PAPER:
            img_send_socket('2.jpg', client_socket)
        
        # server로 부터 전송받을 데이터 길이를 받는다.
        data = client_socket.recv(4)
        # 데이터 길이는 리틀 엔디언 형식으로 int를 변환한다.
        length = int.from_bytes(data, "little")
        # 데이터 길이를 받는다.
        data = client_socket.recv(length)
        if data == b'':
            client_socket.close()
            print(f'[SERVER ERROR] : receive no data')
        # 데이터를 수신한다.
        msg = data.decode()
        # 데이터를 출력한다.
        print('Received from : ', msg)

except Exception as err:
    print(f"[SOCKET ERROR] : {err}")
finally:
    client_socket.close()