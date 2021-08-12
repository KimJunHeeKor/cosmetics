from flask import Blueprint,jsonify
from ..helper.db_connection import db_connect

_fail_dict={'status':'fail','contents':'none'}

bp = Blueprint('curation', __name__, url_prefix='/curation')


host_ip = '14.39.220.155'
user = 'ncyc'
password = 'ncyc0078'
db = 'curation_service'

# 사용자 별 큐레이션 메시지 API
@bp.route('/msg', methods=['GET'])
def curation_msg():
    try:
        rand_num = 101

        sql = f'select * from cur_kw1 where cur_kw1_code = {rand_num}'

        # mysql 접속하고 SQL 전달
        rows = db_connect(host_ip, user, password, db, sql)
        if rows == None:
            json_dict = _fail_dict
        else:
            cur1_dict=[{'field': field, 'type': tp} for field, tp in rows]
            json_dict={'status': 'success', 'contents':cur1_dict}

    except Exception as err:
        print(f'[Error] : {err}')
        json_dict = _fail_dict

    return jsonify(json_dict)