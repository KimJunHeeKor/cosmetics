import time
import random

import statistics

def randomseed():
    seed = random.seed(time.gmtime().tm_sec)
    random.seed(seed)

def analyzed_skin_status():
    
    randomseed()
    
    total_skin_val = random.randint(1,100)
    moisture_val = random.randint(1,100)
    oily_val = random.randint(1,100)
    wrinkle_val = random.randint(1,100)
    pore_val = random.randint(1,100)
    pigm_val = random.randint(1,100)

    userskin_anal_status_dict={
        'Tot' : total_skin_val,#Total skin value : 피부상태분석결과값
        'Mois' : moisture_val, #Moisture : 수분값
        'Oily' : oily_val,     #Oily : 유분값
        'Wrin' : wrinkle_val,  #Winkle : 주름값
        'Pore' : pore_val,     #Pore : 모공값
        'Pigm' : pigm_val,     #Pigmentation : 색소침착값
    }
    return userskin_anal_status_dict

def average_user_skinvalue():
    
    randomseed()

    avg_total_skin_val = round(random.uniform(20.0,80.0), 2)
    avg_moisture_val = round(random.uniform(20.0,80.0), 2)
    avg_oily_val = round(random.uniform(20.0,80.0), 2)
    avg_wrinkle_val = round(random.uniform(20.0,80.0), 2)
    avg_pore_val = round(random.uniform(20.0,80.0), 2)
    avg_pigm_val = round(random.uniform(20.0,80.0), 2)

    userskin_avg_val_dict = {
        'avgTot' : avg_total_skin_val,  #Average total skin value : 평균 피부상태분석결과값
        'avgMois' : avg_moisture_val,   #Average moisture : 평균 수분값
        'avgOily' : avg_oily_val,       #Average oily : 평균 유분값
        'avgWrin' : avg_wrinkle_val,    #Average winkle : 평균 주름값
        'avgPore' : avg_pore_val,       #Average pore : 평균 모공값
        'avgPigm' : avg_pigm_val        #Average pigmentation : 평균 색소침착값
    }

    return userskin_avg_val_dict


def median_users_skinvalue():

    randomseed()

    med_total_skin_val = statistics.median([random.randint(20,80)])
    med_moisture_val = statistics.median([random.randint(20,80)])
    med_oily_val = statistics.median([random.randint(20,80)])
    med_wrinkle_val = statistics.median([random.randint(20,80)])
    med_pore_val = statistics.median([random.randint(20,80)])
    med_pigm_val = statistics.median([random.randint(20,80)])

    userskin_med_val_dict = {
        'medTot' : med_total_skin_val,  #Median total skin value : 중앙 피부상태분석결과값
        'medMois' : med_moisture_val,   #Median moisture : 중앙 수분값
        'medOily' : med_oily_val,       #Median oily : 중앙 유분값
        'medWrin' : med_wrinkle_val,    #Median winkle : 중앙 주름값
        'medPore' : med_pore_val,       #Median pore : 중앙 모공값
        'medPigm' : med_pigm_val        #Median pigmentation : 중앙 색소침착값
    }

    return userskin_med_val_dict

def max_user_skinvalue():

    randomseed()

    max_total_skin_val = max([random.randint(80,100)])
    max_moisture_val = max([random.randint(80,100)])
    max_oily_val = max([random.randint(80,100)])
    max_wrinkle_val = max([random.randint(80,100)])
    max_pore_val = max([random.randint(80,100)])
    max_pigm_val = max([random.randint(80,100)])

    userskin_max_val_dict = {
        'maxTot' : max_total_skin_val,  #Max total skin value : 최대 피부상태분석결과값
        'maxMois' : max_moisture_val,   #Max moisture : 최대 수분값
        'maxOily' : max_oily_val,       #Max oily : 최대 유분값
        'maxWrin' : max_wrinkle_val,    #Max winkle : 최대 주름값
        'maxPore' : max_pore_val,       #Max pore : 최대 모공값
        'maxPigm' : max_pigm_val        #Max pigmentation : 최대 색소침착값
    }

    return userskin_max_val_dict

def min_user_skinvalue():

    randomseed()

    min_total_skin_val = min([random.randint(1,20)])
    min_moisture_val = min([random.randint(1,20)])
    min_oily_val = min([random.randint(1,20)])
    min_wrinkle_val = min([random.randint(1,20)])
    min_pore_val = min([random.randint(1,20)])
    min_pigm_val = min([random.randint(1,20)])

    userskin_min_val_dict = {
        'minTot' : min_total_skin_val,  #Min total skin value : 최소 피부상태분석결과값
        'minMois' : min_moisture_val,   #Min moisture : 최소 수분값
        'minOily' : min_oily_val,       #Min oily : 최소 유분값
        'minWrin' : min_wrinkle_val,    #Min winkle : 최소 주름값
        'minPore' : min_pore_val,       #Min pore : 최소 모공값
        'minPigm' : min_pigm_val        #Min pigmentation : 최소 색소침착값
    }

    return userskin_min_val_dict