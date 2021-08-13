import time
from flask import Blueprint, jsonify

bp = Blueprint('recommend', __name__, url_prefix='/recommend')

# 사용자 별 상품추천 메시지
@bp.route('/msg', methods=['POST'])
def product_recom():
    recomm_products = ['A 제품을 쓰시면 좋을 것 같아요.']
    recom_msg_dict = {'prod':recomm_products }
    json_dict={
        'rt': 'OK', 
        'contents':recom_msg_dict,
        'pubDate':time.strftime('%Y-%M-%d %H:%m:%S')
        }
    return jsonify(json_dict)