from datetime import datetime
import os
import time

from cosmetic.model.db_models import TotalScoreOutput, Submit, UserInfo, db
from sqlalchemy import and_
from sqlalchemy.sql import func


from typing import Dict

def calculate_user_skin_status(user:UserInfo, search_datetime:datetime) -> Dict:

    total_score_output = TotalScoreOutput.query.join(Submit, TotalScoreOutput.s_id == Submit.id)\
                        .filter(and_(Submit.uid == user.id, Submit.created_date == search_datetime )) \
                        .order_by(Submit.created_date.desc()).first_or_404()
    analyzed_dict={
        'Tot' : total_score_output.total_score, #Total skin value : 피부상태분석결과값
        'Mois' : total_score_output.moisture,   #Moisture : 수분값
        'Oily' : total_score_output.oily,       #Oily : 유분값
        'Pore' : total_score_output.pore,       #Pore : 모공값
        'Pigm' : total_score_output.pigment,    #Pigmentation : 색소침착값
        'Sen' : total_score_output.sensitivity  #Sensitivity : 민감도
    }
    return analyzed_dict


def calculate_average_user_skinvalue(column:str, user:UserInfo, search_datetime:datetime) -> Dict:
    
    if column == "yearofbirth":
        user_info = UserInfo.year_of_birth
        compared_user_info = user.year_of_birth
    else:
        return
    avg_total_score = db.session.query(func.avg(TotalScoreOutput.total_score).label("avg_total_skin_val"),\
                        func.avg(TotalScoreOutput.moisture).label("avg_moisture_val"),\
                        func.avg(TotalScoreOutput.oily).label("avg_oily_val"),\
                        func.avg(TotalScoreOutput.pore).label("avg_pore_val"),\
                        func.avg(TotalScoreOutput.pigment).label("avg_pigm_val"),\
                        func.avg(TotalScoreOutput.sensitivity).label("avg_sen_val")). \
                        select_from(Submit). \
                        join(UserInfo, UserInfo.id == Submit.uid). \
                        join(TotalScoreOutput, Submit.id == TotalScoreOutput.s_id). \
                        filter(user_info == compared_user_info, Submit.created_date <= search_datetime).  \
                        first_or_404()
    average_dict = {
        'avgTot' : float(avg_total_score.avg_total_skin_val),  #Average total skin value : 평균 피부상태분석결과값
        'avgMois' : float(avg_total_score.avg_moisture_val),   #Average moisture : 평균 수분값
        'avgOily' : float(avg_total_score.avg_oily_val),       #Average oily : 평균 유분값
        'avgPore' : float(avg_total_score.avg_pore_val),       #Average pore : 평균 모공값
        'avgPigm' : float(avg_total_score.avg_pigm_val),        #Average pigmentation : 평균 색소침착값
        'avgSen' : float(avg_total_score.avg_sen_val)         #Average sensitivity : 평균 민감도
    }
    return average_dict

        

def calculate_max_user_skinvalue(column:str, user:UserInfo, search_datetime:datetime) -> Dict:
    if column == "yearofbirth":
        user_info = UserInfo.year_of_birth
        compared_user_info = user.year_of_birth
    else:
        return
    max_total_score = db.session.query(func.max(TotalScoreOutput.total_score).label("max_total_skin_val"),
                        func.max(TotalScoreOutput.moisture).label("max_moisture_val"),
                        func.max(TotalScoreOutput.oily).label("max_oily_val"),
                        func.max(TotalScoreOutput.pore).label("max_pore_val"),
                        func.max(TotalScoreOutput.pigment).label("max_pigm_val"),
                        func.max(TotalScoreOutput.sensitivity).label("max_sen_val")). \
                        select_from(Submit). \
                        join(UserInfo, UserInfo.id == Submit.uid). \
                        join(TotalScoreOutput, Submit.id == TotalScoreOutput.s_id). \
                        filter(user_info == compared_user_info, Submit.created_date <= search_datetime).  \
                        first_or_404()

    max_dict = {
        'maxTot' : max_total_score.max_total_skin_val,  #Max total skin value : 최대 피부상태분석결과값
        'maxMois' : max_total_score.max_moisture_val,   #Max moisture : 최대 수분값
        'maxOily' : max_total_score.max_oily_val,       #Max oily : 최대 유분값
        'maxPore' : max_total_score.max_pore_val,       #Max pore : 최대 모공값
        'maxPigm' : max_total_score.max_pigm_val,       #Max pigmentation : 최대 색소침착값
        'maxSen' : max_total_score.max_sen_val          #Max sensitivity : 최대 민감도
    }

    return max_dict


def calculate_min_user_skinvalue(column:str, user:UserInfo, search_datetime:datetime) -> Dict:
    if column == "yearofbirth":
        user_info = UserInfo.year_of_birth
        compared_user_info = user.year_of_birth
    else:
        return
    min_total_score = db.session.query(func.min(TotalScoreOutput.total_score).label("min_total_skin_val"),
                        func.min(TotalScoreOutput.moisture).label("min_moisture_val"),
                        func.min(TotalScoreOutput.oily).label("min_oily_val"),
                        func.min(TotalScoreOutput.pore).label("min_pore_val"),
                        func.min(TotalScoreOutput.pigment).label("min_pigm_val"),
                        func.min(TotalScoreOutput.sensitivity).label("min_sen_val")). \
                        select_from(Submit). \
                        join(UserInfo, UserInfo.id == Submit.uid). \
                        join(TotalScoreOutput, Submit.id == TotalScoreOutput.s_id). \
                        filter(user_info == compared_user_info, Submit.created_date <= search_datetime).  \
                        first_or_404()
    min_dict = {
        'minTot' : min_total_score.min_total_skin_val,  #Min total skin value : 최소 피부상태분석결과값
        'minMois' : min_total_score.min_moisture_val,   #Min moisture : 최소 수분값
        'minOily' : min_total_score.min_oily_val,       #Min oily : 최소 유분값
        'minPore' : min_total_score.min_pore_val,       #Min pore : 최소 모공값
        'minPigm' : min_total_score.min_pigm_val,       #Min pigmentation : 최소 색소침착값
        'minSen' : min_total_score.min_sen_val          #Min sensitivity : 최소 민감도
    }

    return min_dict


def convert_url_to_timeformat(input_url:str)->datetime:
    
    year = input_url[:4]
    month = input_url[4:6]
    day = input_url[6:8]
    hour = input_url[8:10]
    minute = input_url[-4:-2]
    second = input_url[-2:]
    time_format = f'{year}-{month}-{day} {hour}:{minute}:{second}'
    search_datetime=datetime.strptime(time_format, "%Y-%m-%d %H:%M:%S")

    return search_datetime

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