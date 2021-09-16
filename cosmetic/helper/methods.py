import os
import time
from datetime import datetime

from cosmetic.model.db_models import TotalScoreOutput, Submit, Survey, UserInfo, db
from sqlalchemy import and_
from sqlalchemy.sql import func


from typing import Dict

def find_or_create_subtmit(acc_id:str)->str:
    uid = db.session.query(UserInfo.id) \
                        .select_from(UserInfo) \
                        .filter(UserInfo.acc_id==acc_id) \
                        .first()
    s_id = db.session.query(Submit.id) \
                        .select_from(Submit) \
                        .filter(Submit.uid == uid[0])  \
                        .order_by(Submit.created_date.desc()) \
                        .first()

    survey = db.session.query(Survey.s_id) \
                        .select_from(Survey) \
                        .filter(Survey.s_id == s_id[0]) \
                        .first()

    if survey != None:

        submit = Submit(uid=uid[0], created_date=datetime.now())
        db.session.add(submit)
        db.session.commit()

        s_id = db.session.query(Submit.id) \
                            .select_from(Submit) \
                            .filter(Submit.uid == uid[0])  \
                            .order_by(Submit.created_date.desc()) \
                            .first()
    return str(s_id[0])

def calculate_user_skin_history(acc_id:str)->list:
    '''
    유저가 피부 평가를 받은 히스토리를 DB에서 리스트로 불러오는 메소드 @20210903 KJH
    @params
    acc_id(str) : 유저 아이디
    
    @return
    skin_history(list) : 유저의 피부측정 히스토리
    '''
    #SQL
    skin_history = db.session.query(Submit.created_date.label('date')) \
                        .select_from(Submit) \
                        .join(UserInfo, UserInfo.id == Submit.uid) \
                        .join(TotalScoreOutput, Submit.id == TotalScoreOutput.s_id) \
                        .filter(UserInfo.acc_id == acc_id)  \
                        .order_by(Submit.created_date.desc()) \
                        .all()
    if skin_history == None:
        return
    
    return skin_history

def calculate_user_skin_status(user:UserInfo, search_datetime:datetime) -> Dict:
    '''
    피부 평가를 받고 나온 점수 결과를 DB에서 가져오는 메소드   @20210903 KJH
    @params
    user(UserInfo) : DB에서 가져온 user정보 개체
    search_datetime(datetime) : 검색하고자 하는 시간
    
    @return
    analyzed_dict(Dict) : 결과 값
    '''
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
    '''
    해당 카테고리에 대한 피부 평가 평균 점수를 DB에서 가져오는 메소드   @20210903 KJH
    @params
    column(str) : 비교 카테고리
    user(UserInfo) : DB에서 가져온 user정보 개체
    search_datetime(datetime) : 검색하고자 하는 시간

    @return
    average_dict(Dict) : 결과 값
    '''
    if column == "yearofbirth":
        user_info = UserInfo.year_of_birth
        compared_user_info = user.year_of_birth
    elif column == "sex":
        user_info = UserInfo.sex
        compared_user_info = user.sex
    elif column == "residence":
        user_info = UserInfo.residence
        compared_user_info = user.residence
    elif column == "nation":
        user_info = UserInfo.nation
        compared_user_info = user.nation
    elif column == "marriage":
        user_info = UserInfo.marriage
        compared_user_info = user.marriage
    elif column == "job":
        user_info = UserInfo.job
        compared_user_info = user.job
    elif column == "education":
        user_info = UserInfo.education
        compared_user_info = user.education
    else:
        return

    '''
    SELECT avg(total_score_output.total_score) AS avg_total_skin_val, 
    avg(total_score_output.moisture) AS avg_moisture_val, avg(total_score_output.oily) AS avg_oily_val, 
    avg(total_score_output.pore) AS avg_pore_val, avg(total_score_output.pigment) AS avg_pigm_val, 
    avg(total_score_output.sensitivity) AS avg_sen_val FROM submit INNER JOIN user_info 
    ON user_info.id = submit.uid INNER JOIN total_score_output ON submit.id = total_score_output.s_id 
    WHERE user_info.year_of_birth = '{user.year_of_birth} AND date_format(submit.created_date, '%Y-%m-%d %H:%i:%S') <= 
    '{search_datetime}' LIMIT 1;
    '''
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
    '''
    해당 카테고리에 대한 피부 평가 최대 점수를 DB에서 가져오는 메소드   @20210903 KJH
    @params
    column(str) : 비교 카테고리
    user(UserInfo) : DB에서 가져온 user정보 개체
    search_datetime(datetime) : 검색하고자 하는 시간

    @return
    max_dict(Dict) : 결과 값
    '''
    if column == "yearofbirth":
        user_info = UserInfo.year_of_birth
        compared_user_info = user.year_of_birth
    elif column == "sex":
        user_info = UserInfo.sex
        compared_user_info = user.sex
    elif column == "residence":
        user_info = UserInfo.residence
        compared_user_info = user.residence
    elif column == "nation":
        user_info = UserInfo.nation
        compared_user_info = user.nation
    elif column == "marriage":
        user_info = UserInfo.marriage
        compared_user_info = user.marriage
    elif column == "job":
        user_info = UserInfo.job
        compared_user_info = user.job
    elif column == "education":
        user_info = UserInfo.education
        compared_user_info = user.education
    else:
        return
    '''
    SELECT max(total_score_output.total_score) AS max_total_skin_val, 
    max(total_score_output.moisture) AS max_moisture_val, max(total_score_output.oily) AS max_oily_val, 
    max(total_score_output.pore) AS max_pore_val, avg(total_score_output.pigment) AS max_pigm_val, 
    max(total_score_output.sensitivity) AS max_sen_val FROM submit INNER JOIN user_info 
    ON user_info.id = submit.uid INNER JOIN total_score_output ON submit.id = total_score_output.s_id 
    WHERE user_info.year_of_birth = '{user.year_of_birth} AND date_format(submit.created_date, '%Y-%m-%d %H:%i:%S') <= 
    '{search_datetime}' LIMIT 1;
    '''
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
    '''
    해당 카테고리에 대한 피부 평가 최소 점수를 DB에서 가져오는 메소드   @20210903 KJH
    @params
    column(str) : 비교 카테고리
    user(UserInfo) : DB에서 가져온 user정보 개체
    search_datetime(datetime) : 검색하고자 하는 시간

    @return
    min_dict(Dict) : 결과 값
    '''
    if column == "yearofbirth":
        user_info = UserInfo.year_of_birth
        compared_user_info = user.year_of_birth
    elif column == "sex":
        user_info = UserInfo.sex
        compared_user_info = user.sex
    elif column == "residence":
        user_info = UserInfo.residence
        compared_user_info = user.residence
    elif column == "nation":
        user_info = UserInfo.nation
        compared_user_info = user.nation
    elif column == "marriage":
        user_info = UserInfo.marriage
        compared_user_info = user.marriage
    elif column == "job":
        user_info = UserInfo.job
        compared_user_info = user.job
    elif column == "education":
        user_info = UserInfo.education
        compared_user_info = user.education
    else:
        return

    '''
    SELECT min(total_score_output.total_score) AS min_total_skin_val, 
    min(total_score_output.moisture) AS min_moisture_val, min(total_score_output.oily) AS min_oily_val, 
    min(total_score_output.pore) AS min_pore_val, avg(total_score_output.pigment) AS min_pigm_val, 
    min(total_score_output.sensitivity) AS min_sen_val FROM submit INNER JOIN user_info 
    ON user_info.id = submit.uid INNER JOIN total_score_output ON submit.id = total_score_output.s_id 
    WHERE user_info.year_of_birth = '{user.year_of_birth} AND date_format(submit.created_date, '%Y-%m-%d %H:%i:%S') <= 
    '{search_datetime}' LIMIT 1;
    '''
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

def convert_datetime_to_str(input_datetime:datetime)->str:
    '''
    datetime을 설정된 문자열로 변환하는 메소드 @20210903 KJH
    @params
    input_datetime(datetime) : datetime 입력값

    @return
    (str) : datetime 포멧의 설정된 문자열
    '''
    return datetime.strftime(input_datetime, "%Y-%m-%d %H:%M:%S")
     
def convert_url_to_timeformat(input_url:str)->datetime:
    '''
    문자열을 설정된 포멧의 datetime로 변환하는 메소드 @20210903 KJH
    @params
    input_url(str) : 입력문자열 (년도월일시분초)

    @return
    search_datetime(datetime) : 설정된 포멧의 datetime
    '''
    year = input_url[:4]
    month = input_url[4:6]
    day = input_url[6:8]
    hour = input_url[8:10]
    minute = input_url[-4:-2]
    second = input_url[-2:]
    time_format = f'{year}-{month}-{day} {hour}:{minute}:{second}'
    search_datetime=datetime.strptime(time_format, "%Y-%m-%d %H:%M:%S")

    return search_datetime

# def make_log_msg(log_result:str, log_msg:str)->str:
#     '''
#     log 메시지 기본 포멧 제공 메서드 @20210902 KJH
#     @params
#     log_result(str) - 실행 결과 메시지
#     log_msg(str)    - 실행 결과 상세 메시지
    
#     @return
#     log_msg(str) : 로그 메시지
#     '''
#     log_msg = f'[{time_log()}] [{log_result}] : {log_msg}'
#     return log_msg

def msg_dict(rt:str, content:Dict=None) -> Dict:
    '''
    JSON 메시지를 위한 고정된 딕셔러니 제작 메소드 @20210824 KJH  
    @params
    rt(str) : 성공결과
    content(Dict) : API 전달 내용

    @return
    json_dict (json) : API json
    '''
    json_dict = {'rt': rt ,'pubDate': datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')}
    if content is not None:
        json_dict['contents'] = content
    return json_dict

class save_log:
    '''
    로그 저장 @20210823 KJH
    @params
    log_result(str) - 실행 결과 메시지
    log_msg(str)    - 실행 결과 상세 메시지
    error(bool) :  에러 메시지 저장 여부
    '''
    error = False
    base_path = os.getcwd()+'/cosmetic/log'
    year = datetime.strftime(datetime.now(),'%Y')
    month_day = datetime.strftime(datetime.now(),'%m.%d')
    log_file_name = "log.txt"
    error_log_file_name = "error_log.txt"

    @classmethod
    def info(cls, log_message:str, error:bool=False):
        cls._save_logging("INFO", log_message, error=error)

    @classmethod
    def error(cls, log_message:str, error:bool=False):
        cls._save_logging("ERROR", log_message, error=error)

    @classmethod
    def critical(cls, log_message:str, error:bool=False):
        cls._save_logging("CRITICAL", log_message, error=error)

    @classmethod
    def debug(cls, log_message:str, error:bool=False):
        cls._save_logging("DEBUG", log_message, error=error)

    @classmethod
    def warning(cls, log_message:str, error:bool=False):
        cls._save_logging("WARNING", log_message, error=error)

    @classmethod
    def _save_logging(cls, log_rt:str, log_msg:str, error:bool=False):
        try:
            if not os.path.exists(cls.base_path):
                os.makedirs(cls.base_path)

            if not os.path.exists(cls.base_path+'/'+cls.year):
                os.makedirs(cls.base_path+'/'+cls.year)

            if not os.path.exists(cls.base_path+'/'+cls.year+'/'+cls.month_day):
                os.makedirs(cls.base_path+'/'+cls.year+'/'+cls.month_day)

            log_messsage = cls._make_log_msg(log_rt, log_msg)
            f = open(cls.base_path+'/'+cls.year+'/'+cls.month_day+'/'+cls.log_file_name, 'a+',encoding='utf8')
            f.write(log_messsage+'\n')
            f.close()

            if error:
                err_log_msg = cls._make_log_msg(log_rt, log_msg)
                err_file = open(cls.base_path+'/'+cls.year+'/'+cls.month_day+'/'+cls.error_log_file_name, 'a+',encoding='utf8')
                err_file.write(err_log_msg+"\n")
                err_file.close()

            print(log_messsage)

        except Exception as err:
            
            exc_log_msg = cls._make_log_msg("ERROR", "SAVE LOG - "+ err)
            except_file = open(cls.base_path+'/'+cls.year+'/'+cls.month_day+'/'+cls.error_log_file_name, 'a+',encoding='utf8')
            except_file.write(exc_log_msg+"\n")
            except_file.close()

            print(exc_log_msg)

    @classmethod
    def _make_log_msg(cls, log_result:str, log_msg:str)->str:
        '''
        log 메시지 기본 포멧 제공 메서드 @20210902 KJH
        @params
        log_result(str) - 실행 결과 메시지
        log_msg(str)    - 실행 결과 상세 메시지
        
        @return
        log_msg(str) : 로그 메시지
        '''
        log = f'[{time_log()}] [{log_result}] : {log_msg}'
        return log

def time_log() -> str:
    '''
    로그 시간을 기록하기 위한 메소드 @20210823 KJH
    @return
    time (str) : %Y-%m-%d %H:%m:%S 형태의 시간
    '''
    return datetime.strftime(datetime.now(),'%Y-%m-%d %H:%M:%S')