import time
import random

from flask import Blueprint,jsonify
from cosmetic.model.db_models import CurKw1, CurKw2

_fail_dict={
    'rt':'fail',
    'contents':'none',
    'pubDate':time.strftime('%Y-%M-%d %H:%m:%S')
    }

bp = Blueprint('curation', __name__, url_prefix='/curation')


# 사용자 별 큐레이션 메시지 API
@bp.route('/msg', methods=['POST'])
def curation_msg():
    try:
        rand_code = [
            (101, 11),(102, 11), (103,11), (104,11), (105, 21), 
            (901, 31),(902, 31),(903, 31), (904,31), (905, 31)
            ]
        rand_idx = random.randint(0, 10)
        
        #select query
        kw1_msg = CurKw1.query.filter_by(cur_kw1_id= rand_code[rand_idx][0]).first()
        kw2_msg = CurKw2.query.filter_by(cur_kw2_id= rand_code[rand_idx][1]).first()

        if kw1_msg == None:
            json_dict = _fail_dict
        else:
            json_dict={
                'rt':'OK',
                'contents':{
                    'msg': f'{kw1_msg.cur_kw1_msg}을(를) {kw2_msg.cur_kw2_msg}세요.'
                },
                'pubDate':time.strftime('%Y-%M-%d %H:%m:%S')
            }

    except Exception as err:
        print(f'[Error] : {err}')
        json_dict = _fail_dict

    return jsonify(json_dict)