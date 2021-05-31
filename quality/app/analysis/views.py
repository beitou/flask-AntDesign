from flask import request
from flask import jsonify

from app.analysis.service import Service

from app.analysis import analysis


@analysis.route('/analysis/api/v1/save_jira_bugs', methods=['GET', 'POST'])
def save_jira_bugs():

    if request.method == 'GET':
        data = request.values.to_dict()
    else:
        data = request.get_json()

    try:
        service = Service()
        result = service.save_jira_bugs(data)
        return jsonify({
            'status': 0,
            'message': u'状态更新成功',
            'data': result
        })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': u'系统错误,请重试',
            'data': {
              'error': str(error)
            }
        })


@analysis.route('/analysis/api/v1/save_code_lines', methods=['GET', 'POST'])
def save_code_lines():

    if request.method == 'GET':
        data = request.values.to_dict()
    else:
        data = request.get_json()

    try:
        service = Service()
        result = service.save_code_lines(data)
        return jsonify({
            'status': 0,
            'message': u'状态更新成功',
            'data': result
        })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': u'系统错误,请重试',
            'data': {
              'error': str(error)
            }
        })


@analysis.route('/analysis/api/v1/search', methods=['GET', 'POST'])
def search_product_quality_data():
    """
    :return:
    """
    if request.method == 'GET':
        data = request.values.to_dict()
    else:
        data = request.get_json()

    try:
        service = Service()
        result = service.search(data)
        return jsonify({
            'status': 0,
            'message': '查询数据成功！',
            'data': result
        })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': u'系统错误,请重试',
            'data': {
                'error': str(error)
            }
        })
