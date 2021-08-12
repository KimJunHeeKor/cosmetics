from flask import Blueprint, jsonify
bp = Blueprint('product_recommand', __name__, url_prefix='/product')

# 사용자 별 상품추천 메시지
@bp.route('/recommand', methods=['GET'])
def product_recom():
    recom_msg_dict = [{'product':'A'}, {'product':'B'},{'product':'C'}]
    json_dict={'status': 'success', 'contents':recom_msg_dict}
    return jsonify(json_dict)