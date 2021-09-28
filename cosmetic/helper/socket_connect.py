import socket
from io import BytesIO

from cosmetic.helper.methods import *

FULL_FACE='FULL_FACE'
OIL_PAPER='OIL_PAPER'
SURVEY = 'SURVEY'

def rev_msg_socket(client_socket:socket) -> str:
    '''
    소켓통신으로 데이터 받는 메소드@20210830 KJH
    @param
    client_socket(socket) : 클라이언트 소켓
    @return
    msg(str) : 소켓통신으로 받은 메시지
    '''
    # server로 부터 전송받을 데이터 길이를 받는다.
    data = client_socket.recv(4)
    # 데이터 길이는 리틀 엔디언 형식으로 int를 변환한다.
    length = int.from_bytes(data, "little")
    # 데이터 길이를 받는다.
    data = client_socket.recv(length)
    # 데이터를 수신한다.
    msg = data.decode()
    
    save_log.info(f"(RECEIVE SUCCESS) {msg}")

    return msg

def send_msg_socket(msg:str, client_socket:socket):
    '''
    소켓통신을 통해 메시지 전달 메소드 @20210830 KJH
    @params
    msg(str): 전달 메시지
    client_socket(socket): 클라이언트 전송 소켓
    '''
    # 메시지 인코딩
    encode_msg = msg.encode()
    # 메시지 길이 전달
    encode_msg_len = len(encode_msg)
    client_socket.sendall(encode_msg_len.to_bytes(4, byteorder="little"))
    # 해당 메시지 전달
    client_socket.sendall(encode_msg)
    save_log.info(f"(MESSAGE SEND SUCCESS) {msg}")

def send_img_socket(load_file_path:str, client_socket:socket, buffer_size:int=1024):
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

    if str(type(load_file_path)) == "<class 'werkzeug.datastructures.FileStorage'>":
        send_file = BytesIO(load_file_path.stream.read())
    else:
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
    send_file.close()
    save_log.info(f"(IMAGE SEND SUCCESS) {load_file_path.filename}")