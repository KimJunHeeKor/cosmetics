import random
import time
import statistics

from flask import Blueprint, jsonify, request
from ..lib.userskin_mths import analyzed_skin_status, average_user_skinvalue, median_users_skinvalue, max_user_skinvalue, min_user_skinvalue

_fail_dict={
    'rt':'fail',
    'contents':'none',
    'pubDate':time.strftime('%Y-%M-%d %H:%m:%S')
    }

bp = Blueprint('userskin', __name__, url_prefix='/userskin')

# 피부분석 결과 API
@bp.route('/values', methods=['POST'])
def userskin_anal_status():
    if request.method != 'POST':
        return jsonify(_fail_dict)

    analyzed_dict = analyzed_skin_status()
    average_dict = average_user_skinvalue()
    median_dict = median_users_skinvalue()
    max_dict = max_user_skinvalue()
    min_dict = min_user_skinvalue()

    json_dict={
        'rt':'OK',
        'contents': {
            'anal':analyzed_dict,
            'avg':average_dict,
            'med':median_dict,
            'max':max_dict,
            'min':min_dict
        },
        'pubDate':time.strftime('%Y-%M-%d %H:%m:%S')
    }
    

    return jsonify(json_dict)