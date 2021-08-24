# 소켓을 사용하기 위해서는 socket을 import해야 한다.
import socket
import base64
import cv2
import numpy
from PIL import Image
# 로컬은 127.0.0.1의 ip로 접속한다.
HOST = 'localhost'
# HOST = '14.39.220.155'
# port는 위 서버에서 설정한 9999로 접속을 한다.
PORT = 9999
# PORT= 34512
# 소켓을 만든다.
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket = socket.socket()
# connect함수로 접속을 한다.
client_socket.connect((HOST, PORT))

try:
    # 10번의 루프로 send receive를 한다.
    for i in range(1):
    # 메시지는 hello로 보낸다.
        # img = numpy.array(Image.open('1.jpg'))
        # resize_frame = cv2.resize(img, dsize=(50, 20), interpolation=cv2.INTER_AREA)

        # encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
        # result, imgencode = cv2.imencode('.jpg', resize_frame, encode_param)
        # result, imgencode = cv2.imencode('.jpg', img)
        # 
        # data = numpy.array(imgencode)
        # # stringData = base64.b64encode(data)
        # stringData = data.tobytes()
        '''
        file = open('1.jpg', 'rb')
        image_data = file.read(2048)
        while image_data:
            client_socket.send(image_data)
            image_data = file.read(2048)
        file.close()
        '''
        msg = 'hello'
        # 메시지를 바이너리(byte)형식으로 변환한다.
        data = msg.encode()
        # 메시지 길이를 구한다.
        length = len(data)
        # server로 리틀 엔디언 형식으로 데이터 길이를 전송한다.
        client_socket.sendall(length.to_bytes(4, byteorder="little"))
        # 데이터를 전송한다.
        client_socket.sendall(data)
        # server로 부터 전송받을 데이터 길이를 받는다.
        data = client_socket.recv(4)
        # 데이터 길이는 리틀 엔디언 형식으로 int를 변환한다.
        length = int.from_bytes(data, "little")
        # 데이터 길이를 받는다.
        data = client_socket.recv(length)
        if data == b'':
            client_socket.close()
            print(f'[SERVER ERROR] : receive no data')
            break
        # 데이터를 수신한다.
        msg = data.decode()
        # 데이터를 출력한다.
        print('Received from : ', msg)
except Exception as err:
    print(f"[SOCKET ERROR] : {err}")
finally:
    client_socket.close()