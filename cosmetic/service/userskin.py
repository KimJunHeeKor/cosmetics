from datetime import datetime

from cosmetic.helper.methods import *
from cosmetic.lib.userskin_mths import analyzed_skin_status, average_user_skinvalue, median_users_skinvalue, max_user_skinvalue, min_user_skinvalue
from cosmetic.model.db_models import UserInfo



from flask import Blueprint, jsonify, request
from flask_jwt_extended import *

bp = Blueprint('userskin', __name__, url_prefix='/userskin')

@bp.route('/values', methods=['POST'])
def userskin_anal_status():
    '''
    피부분석 결과 전달 API
    '''
    if request.method != 'POST':
        return jsonify(msg_dict('fail', 'POST 전송이 아닙니다.'))

    analyzed_dict = analyzed_skin_status()
    average_dict = average_user_skinvalue()
    median_dict = median_users_skinvalue()
    max_dict = max_user_skinvalue()
    min_dict = min_user_skinvalue()

    return jsonify(msg_dict('ok', {
            'anal': analyzed_dict,
            'avg': average_dict,
            'med': median_dict,
            'max': max_dict,
            'min': min_dict
        }))

@bp.route("/values/history", methods=["GET"])
@jwt_required(fresh=True)
def search_user_skin_history():
    '''
    사용자에 대한 피부정보 측정 히스토리 전달 API
    '''
    try:
        acc_id = get_jwt_identity()
        user_history_date=[]
        
        user_history = calculate_user_skin_history(acc_id)
        
        for history in user_history:
            user_history_date.append(datetime.strftime(history.date, "%Y-%m-%d %H:%M:%S"))
        save_log.info(f"(SEARCH USER SKIN HISTORY) ({acc_id}) 사용자의 피부 히스토리를 불러왔습니다.")
        return jsonify(msg_dict("ok", {'history':user_history_date})), 200

    except Exception as err:
        save_log.error(f"(SEARCH USER SKIN HISTORY) {err}", error=True)
        return jsonify(msg_dict('fail')), 400


@bp.route('/values/filter', methods=['GET'])
@jwt_required(fresh=True)
def seach_user_skin_values():
    '''
    사용자에 대한 피부정보를 전달해주는 API
    '''
    try:

        sql_condition_dict = {}
        #전송된 데이터를 변수에 저장
        yearofbirth = request.args.get("yearofbirth")
        sex = request.args.get("sex")
        residence = request.args.get("residence")
        nation = request.args.get("nation")
        marriage = request.args.get("marriage")
        job = request.args.get("job")
        education = request.args.get("education")
        search_date = request.args.get("search_date")


        if yearofbirth != None and yearofbirth != "":
            sql_condition_dict["UserInfo.year_of_birth"] = yearofbirth
        if sex != None and sex != "":
            sql_condition_dict["UserInfo.sex"] = sex
        if residence != None and residence != "":
            sql_condition_dict["UserInfo.residence"] = residence
        if nation != None and nation != "":
            sql_condition_dict["UserInfo.nation"] = nation
        if marriage != None and marriage != "":
            sql_condition_dict["UserInfo.marriage"] = marriage
        if job != None and job != "":
            sql_condition_dict["UserInfo.job"] = job
        if education != None and education != "":
            sql_condition_dict["UserInfo.education"] = education

        #유저 id를 토큰으로 얻고 전달받은 시간정보를 설정된 datetime 형태로 변환
        acc_id = get_jwt_identity()
        search_datetime = convert_url_to_timeformat(search_date)

        # 해당 유저의 정보를 DB에서 찾는다.
        user = UserInfo.query.filter(UserInfo.acc_id == acc_id).first_or_404()
        if user is None:
            save_log.error(f"(SEARCH USER SKIN VALUES) ({acc_id})사용자를 검색하지 못했습니다.", error=True)
            return jsonify(msg_dict('fail')), 400
        
        
        #DB에서 값 받아오기
        analyzed_dict = calculate_user_skin_status(user, search_datetime)
        average_dict = calculate_average_user_skinvalue(user, search_datetime, **sql_condition_dict)
        max_dict = calculate_max_user_skinvalue(user, search_datetime, **sql_condition_dict)
        min_dict = calculate_min_user_skinvalue(user, search_datetime, **sql_condition_dict)
        save_log.info(f"(SEARCH USER SKIN VALUES SUCCESS) ({acc_id})사용자의 피부상태, 평균값, 최대값, 최소값을 DB에서 가져왔습니다.")

        return jsonify(msg_dict('ok', {
                'anal': analyzed_dict,
                'avg': average_dict,
                'max': max_dict,
                'min': min_dict
            }))
    except Exception as err:
        save_log.error(f"(SEARCH USER SKIN VALUES) {err}", error=True)
        return jsonify(msg_dict('fail')), 400