import os
import time

from typing import Dict


def time_log() -> str:
    '''
    로그 시간을 기록하기 위한 메소드 @20210823 KJH
    @return
    time (str) : %Y-%m-%d %H:%m:%S 형태의 시간
    '''
    return time.strftime('%Y-%m-%d %H:%m:%S')


def msg_dict(rt:str, content:Dict=None) -> Dict:
    '''
    JSON 메시지를 위한 고정된 딕셔러니 제작 메소드 @20210824 KJH  
    @params
    rt(str) : 성공결과
    content(Dict) : API 전달 내용

    @return
    json_dict (json) : API json
    '''
    json_dict = {'rt': rt ,'pubDate': time.strftime('%Y-%m-%d %H:%m:%S')}
    if content is not None:
        json_dict['contents'] = content
    return json_dict


def save_log(msg:str):
    '''
    로그 저장 @20210823 KJH
    @params
    msg (str) : 저장될 메시지
    '''
    base_path = os.getcwd()+'/cosmetic/log'
    year = time.strftime('%Y')
    month_day = time.strftime('%m.%d')
    file_name = 'log.txt'
    try:
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        if not os.path.exists(base_path+'/'+year):
            os.makedirs(base_path+'/'+year)

        if not os.path.exists(base_path+'/'+year+'/'+month_day):
            os.makedirs(base_path+'/'+year+'/'+month_day)

        f = open(base_path+'/'+year+'/'+month_day+'/'+file_name, 'a+',encoding='utf8')
        f.write(msg+'\n')
    except Exception as err:
        err_msg = f'[SIGNUP ERROR] [{time_log()}]: {err}'
        print(err_msg)
        save_error_log(err_msg)
    finally:
        f.close()
        print(msg)


def save_error_log(msg:str):
    '''
    에러로그 저장 @20210823 KJH
    @params
    msg (str) : 저장될 메시지
    '''
    base_path = os.getcwd()+'/cosmetic/log'
    year = time.strftime('%Y')
    month_day = time.strftime('%m.%d')
    file_name = 'error_log.txt'
    try:
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        if not os.path.exists(base_path+'/'+year):
            os.makedirs(base_path+'/'+year)

        if not os.path.exists(base_path+'/'+year+'/'+month_day):
            os.makedirs(base_path+'/'+year+'/'+month_day)

        f = open(base_path+'/'+year+'/'+month_day+'/'+file_name, 'a+',encoding='utf8')
        f.write(msg+'\n')
        f.close()
        print(msg)
    except Exception as err:
        err_msg = f'[SAVE ERRORLOG ERROR] [{time_log()}]: {err}'
        print(err_msg)
        save_error_log(err_msg)