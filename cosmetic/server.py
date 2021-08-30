import time

# 소켓을 사용하기 위해서는 socket을 import해야 한다.
import socket, threading
from typing import Tuple

def current_mill_sec()->int:
    '''
    단위가 ms인 현재시간을 확인하는 메소드 @20210823 KJH

    @return
    millis(int) : ms 단위의 현재 시간 
    '''
    millis = int(round(time.time() * 1000))
    return millis


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
    return msg

def save_img_socket(save_file_path:str, client_socket:socket, buffer_size:int=1024)->Tuple[bool,str]:
    '''
    소켓 통신으로 클라이언트로부터 받은 이미지를 저장하는 메소드 @20210825 KJH

    @params
    save_file_path(str) : 받은 이미지를 저장하는 경로
    client_socket(socket) : 클라이언트 소켓

    @return
    tuple(rt, msg)
        rt(bool) : 저장결과
        msg(str) : 저장결과 메시지
    '''
    try:
        save_msg = ''
        #저장할 파일 위치 생성
        file = open(save_file_path, 'wb')
        rt = False
        
        #이미지 데이터 길이를 확인하기 위한 소켓 통신 (클라이언트에서 보내줘야 함.)
        data = client_socket.recv(4)

        # 소켓 통신으로 받은 이미지 데이터 길이는 4byte로 형태는 byte이다.
        # 이를 int형을 변환
        length = int.from_bytes(data, "little")

        # buffer size만큼 이미지 더미를 받음.(클라이언트가 보낸 크기와 동일해야 함.)
        image_chunk= client_socket.recv(buffer_size)
        # 통신받은 데이터의 길이를 확인
        buffer_length = len(image_chunk)

        
        # 통신으로 받은 데이터가 있는 경우
        while image_chunk:
            # 이미지 더미를 파일에 저장
            file.write(image_chunk)
            # 클라이언트가 보내는 이미지 데이터를 계속해서 받음.
            image_chunk = client_socket.recv(buffer_size)
            # 통신으로 받은 데이터 길이를 누적
            buffer_length += len(image_chunk)
            # 이미지 데이터의 총 길이와 지금까지 받은 데이터의 길이를 비교
            if buffer_length >= length:
                rt = True
                break
        file.close()
        save_msg = f'Image transfer success'
        
    except Exception as err:
        rt = False
        save_msg = f'[IMAGE TRANSFER ERROR] : {err}'

    finally:
        return rt, save_msg

class MessageMapping():
    '''
    메시지 매핑 클래스 @20210825 KJH
    '''
    def __init__(self):
        self.FULL_FACE="FULL_FACE"
        self.OIL_PAPER="OIL_PAPER"
        self.SURVEY = "SURVEY"


def binder(client_socket:socket, addr:str):
    '''
    binder함수는 서버에서 accept가 되면 생성되는 socket 인스턴스를 통해 client로 부터 데이터를 받으면 echo형태로 재송신하는 메소드
    @params
    client_socket(socket) : 클라이언트 소켓
    addr(str) : 클라이언트 주소
    '''
    # 커넥션이 되면 접속 주소가 나온다.
    print('Connected by', addr)
    try:
        # 접속 상태에서는 클라이언트로 부터 받을 데이터를 무한 대기한다.
        # 만약 접속이 끊기게 된다면 except가 발생해서 접속이 끊기게 된다.
        while True:
            start = current_mill_sec()
            msg = rev_msg_socket(client_socket)
            if msg == '':
                return
            uid = None
            msg_mapping=MessageMapping()
            # 이미지 전달 메시지를 받았을 경우 코드가 실행
            if msg == msg_mapping.FULL_FACE:
                acc_id = rev_msg_socket(client_socket)
                device_info = rev_msg_socket(client_socket)
                rt, msg1 = save_img_socket(acc_id+'_full.jpg', client_socket)
            elif msg == msg_mapping.OIL_PAPER:
                rt, msg2 = save_img_socket(acc_id+'_oily.jpg', client_socket)
                print(rt, msg2)
            elif msg == msg_mapping.SURVEY:
                msg2 = rev_msg_socket(client_socket)
                print(msg2)
            
            
            # 수신된 메시지를 콘솔에 출력한다.
            print(f'Received from [host] {addr[0]}, [PORT] {addr[1]} : {msg}')
            # 수신된 메시지 앞에 「echo:」 라는 메시지를 붙힌다.
            msg = 'finish'
            # 바이너리(byte)형식으로 변환한다.
            data = msg.encode()
            # 바이너리의 데이터 사이즈를 구한다.
            length = len(data)
            # 데이터 사이즈를 little 엔디언 형식으로 byte로 변환한 다음 전송한다.
            client_socket.sendall(length.to_bytes(4, byteorder="little"))
            # 데이터를 클라이언트로 전송한다.
            client_socket.sendall(data)
            one_cycle_time  = current_mill_sec() - start
            print(f"[TAKING THE TIME]\tTo AI:ms\tTo A cycle of MSG connection:{one_cycle_time} ms")
    except Exception as err:
        # 접속이 끊기면 except가 발생한다.
        print("except : " , addr, err)
    finally:
        # 접속이 끊기면 socket 리소스를 닫는다.
        client_socket.close()
# 소켓을 만든다.
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# 소켓 레벨과 데이터 형태를 설정한다.
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# 서버는 복수 ip를 사용하는 pc의 경우는 ip를 지정하고 그렇지 않으면 None이 아닌 ''로 설정한다.
# 포트는 pc내에서 비어있는 포트를 사용한다. cmd에서 netstat -an | find "LISTEN"으로 확인할 수 있다.
server_socket.bind(('', 9999))
# server 설정이 완료되면 listen를 시작한다.
server_socket.listen()

try:
    # 서버는 여러 클라이언트를 상대하기 때문에 무한 루프를 사용한다.
    while True:
        # client로 접속이 발생하면 accept가 발생한다.
        # 그럼 client 소켓과 addr(주소)를 튜플로 받는다.
        client_socket, addr = server_socket.accept()
        # 쓰레드를 이용해서 client 접속 대기를 만들고 다시 accept로 넘어가서 다른 client를 대기한다.
        th = threading.Thread(target=binder, args = (client_socket,addr))
        th.start()
except:
    print("server")
finally:
    # 에러가 발생하면 서버 소켓을 닫는다.
    server_socket.close()