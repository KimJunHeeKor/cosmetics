import time
from datetime import datetime

def time_log():
    '''
    로그 시간을 기록하기 위한 메소드 @20210823 KJH
    '''
    return time.strftime('%Y-%M-%d %H:%m:%S')

def msg_dict(rt, content=None):
    '''
    JSON 메시지를 위한 고정된 딕셔러니 제작 메소드 @20210824 KJH  
    '''
    json_dict = {'rt': rt ,'pubDate': time.strftime('%Y-%M-%d %H:%m:%S')}
    if content is not None:
        json_dict['contents'] = content
    return json_dict