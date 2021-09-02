import os
import time

from typing import Dict



def make_log_msg(log_result:str, log_msg:str)->str:
    '''
    log 메시지 기본 포멧 제공 메서드 @20210902 KJH
    @params
    log_result(str) - 실행 결과 메시지
    log_msg(str)    - 실행 결과 상세 메시지
    
    @return
    log_msg(str) : 로그 메시지
    '''
    log_msg = f'[{time_log()}] [{log_result}] : {log_msg}'
    return log_msg

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


def save_log(log_msg:str, log_result:str, error:bool=False):
    '''
    로그 저장 @20210823 KJH
    @params
    log_result(str) - 실행 결과 메시지
    log_msg(str)    - 실행 결과 상세 메시지
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
        log_msg = make_log_msg(log_msg, log_result)
        f = open(base_path+'/'+year+'/'+month_day+'/'+log_file_name, 'a+',encoding='utf8')
        f.write(log_msg+'\n')
        f.close()

        if error:
            err_log_msg = make_log_msg(log_msg, log_result)
            err_file = open(base_path+'/'+year+'/'+month_day+'/'+error_log_file_name, 'a+',encoding='utf8')
            err_file.write(err_log_msg+"\n")
            err_file.close()

        print(log_msg)

    except Exception as err:
        
        exc_log_msg = make_log_msg('SAVE LOG ERROR', err)
        except_file = open(base_path+'/'+year+'/'+month_day+'/'+error_log_file_name, 'a+',encoding='utf8')
        except_file.write(exc_log_msg+"\n")
        except_file.close()

        print(exc_log_msg)

def time_log() -> str:
    '''
    로그 시간을 기록하기 위한 메소드 @20210823 KJH
    @return
    time (str) : %Y-%m-%d %H:%m:%S 형태의 시간
    '''
    return time.strftime('%Y-%m-%d %H:%m:%S')