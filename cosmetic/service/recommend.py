import time
import random

from flask import Blueprint, jsonify

bp = Blueprint('recommend', __name__, url_prefix='/recommend')

def randomseed():
    seed = random.seed(time.gmtime().tm_sec)
    random.seed(seed)

# 사용자 별 상품추천 메시지
@bp.route('/msg', methods=['POST'])
def product_recom():
    randomseed()
    random_products = ['A', 'B', 'C']
    rand_int = random.randint(0,2)
    recomm_products = [f'{random_products[rand_int]} 제품을 쓰시면 좋을 것 같아요.']
    recom_msg_dict = {'prod':recomm_products }
    json_dict={
        'rt': 'OK', 
        'contents':recom_msg_dict,
        'pubDate':time.strftime('%Y-%M-%d %H:%m:%S')
        }
    return jsonify(json_dict)