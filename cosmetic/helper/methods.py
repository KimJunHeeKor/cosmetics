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


def save_log(log_msg:str, error:bool=False):
    '''
    로그 저장 @20210823 KJH
    @params
    msg (str) : 저장될 메시지
    error(bool) :  에러 메시지 저장 여부
    '''
    base_path = os.getcwd()+'/cosmetic/log'
    year = time.strftime('%Y')
    month_day = time.strftime('%m.%d')
    log_file_name = "log.txt"
    error_log_file_name = "error_log.txt"
    try:
        if not os.path.exists(base_path):
            os.makedirs(base_path)

        if not os.path.exists(base_path+'/'+year):
            os.makedirs(base_path+'/'+year)

        if not os.path.exists(base_path+'/'+year+'/'+month_day):
            os.makedirs(base_path+'/'+year+'/'+month_day)

        f = open(base_path+'/'+year+'/'+month_day+'/'+log_file_name, 'a+',encoding='utf8')
        f.write(log_msg+'\n')
        f.close()
        if error is True:
            file = open(base_path+'/'+year+'/'+month_day+'/'+error_log_file_name, 'a+',encoding='utf8')
            file.write(log_msg+"\n")
            file.close()
    except Exception as err:
        log_msg = f'[SAVE LOG ERROR] [{time_log()}]: {err}'
        err_file = open(base_path+'/'+year+'/'+month_day+'/'+error_log_file_name, 'a+',encoding='utf8')
        err_file.write(log_msg+"\n")
        err_file.close()
    finally:
        if not f.closed:
            f.close()
        if not file.closed:
            file.close()
        print(log_msg)