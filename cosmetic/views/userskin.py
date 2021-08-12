import random
import time
import statistics

from flask import Blueprint, jsonify, request
from ..helper.db_connection import db_connect

_fail_dict={'status':'fail','contents':'none'}

bp = Blueprint('userskin', __name__, url_prefix='/userskin')

# 피부분석 결과 API
@bp.route('/analysisval', methods=['GET'])
def userskin_anal_status():
    if request.method != 'GET':
        return jsonify(_fail_dict)

    seed = random.seed(time.gmtime().tm_sec)
    random.seed(seed)
    
    total_skin_val = random.randint(1,100)
    moisture_val = random.randint(1,100)
    oily_val = random.randint(1,100)
    wrinkle_val = random.randint(1,100)
    pore_val = random.randint(1,100)
    pigm_val = random.randint(1,100)

    userskin_anal_status_dict={
        'total_skin_val' : total_skin_val,
        'moisture_val' : moisture_val,
        'oily_val' : oily_val,
        'wrinkle_val' : wrinkle_val,
        'pore_val' : pore_val,
        'pigm_val' : pigm_val,
    }

    json_dict={'status': 'success', 'contents':userskin_anal_status_dict}

    return jsonify(json_dict)

# 사용자군의 피부분석결과에 대한 평균값 API
@bp.route('/avgval', methods=['GET'])
def userskin_avg_val():
    
    seed = random.seed(time.gmtime().tm_sec)
    random.seed(seed)

    avg_total_skin_val = round(random.uniform(1.0,100.0), 2)
    avg_moisture_val = round(random.uniform(1.0,100.0), 2)
    avg_oily_val = round(random.uniform(1.0,100.0), 2)
    avg_wrinkle_val = round(random.uniform(1.0,100.0), 2)
    avg_pore_val = round(random.uniform(1.0,100.0), 2)
    avg_pigm_val = round(random.uniform(1.0,100.0), 2)

    userskin_avg_val_dict = {
        'avg_total_skin_val' : avg_total_skin_val,
        'avg_moisture_val' : avg_moisture_val,
        'avg_oily_val' : avg_oily_val,
        'avg_wrinkle_val' : avg_wrinkle_val,
        'avg_pore_val' : avg_pore_val,
        'avg_pigm_val' : avg_pigm_val
    }

    json_dict={'status': 'success', 'contents':userskin_avg_val_dict}
    return jsonify(json_dict)


#사용자군의 피부분석결과에 대한 중앙값 API
@bp.route('/medianval', methods=['GET'])
def userskin_med_val():
    
    med_total_skin_val = statistics.median([random.randint(1,100)])
    med_moisture_val = statistics.median([random.randint(1,100)])
    med_oily_val = statistics.median([random.randint(1,100)])
    med_wrinkle_val = statistics.median([random.randint(1,100)])
    med_pore_val = statistics.median([random.randint(1,100)])
    med_pigm_val = statistics.median([random.randint(1,100)])

    userskin_med_val_dict = {
        'med_total_skin_val' : med_total_skin_val,
        'med_moisture_val' : med_moisture_val,
        'med_oily_val' : med_oily_val,
        'med_wrinkle_val' : med_wrinkle_val,
        'med_pore_val' : med_pore_val,
        'med_pigm_val' : med_pigm_val
    }

    json_dict={'status': 'success', 'contents':userskin_med_val_dict}
    return jsonify(json_dict)

# 사용자군의 피부분석결과에 대한 최대값 API
@bp.route('/maxval', methods=['GET'])
def userskin_max_val():
    
    max_total_skin_val = max([random.randint(1,100)])
    max_moisture_val = max([random.randint(1,100)])
    max_oily_val = max([random.randint(1,100)])
    max_wrinkle_val = max([random.randint(1,100)])
    max_pore_val = max([random.randint(1,100)])
    max_pigm_val = max([random.randint(1,100)])

    userskin_max_val_dict = {
        'max_total_skin_val' : max_total_skin_val,
        'max_moisture_val' : max_moisture_val,
        'max_oily_val' : max_oily_val,
        'max_wrinkle_val' : max_wrinkle_val,
        'max_pore_val' : max_pore_val,
        'max_pigm_val' : max_pigm_val
    }

    json_dict={'status': 'success', 'contents':userskin_max_val_dict}
    return jsonify(json_dict)

# 사용자군의 피부분석결과에 대한 최소값 API
@bp.route('/minval', methods=['GET'])
def userskin_min_val():
    
    min_total_skin_val = min([random.randint(1,100)])
    min_moisture_val = min([random.randint(1,100)])
    min_oily_val = min([random.randint(1,100)])
    min_wrinkle_val = min([random.randint(1,100)])
    min_pore_val = min([random.randint(1,100)])
    min_pigm_val = min([random.randint(1,100)])

    userskin_min_val_dict = {
        'min_total_skin_val' : min_total_skin_val,
        'min_moisture_val' : min_moisture_val,
        'min_oily_val' : min_oily_val,
        'min_wrinkle_val' : min_wrinkle_val,
        'min_pore_val' : min_pore_val,
        'min_pigm_val' : min_pigm_val
    }

    json_dict={'status': 'success', 'contents':userskin_min_val_dict}
    return jsonify(json_dict)