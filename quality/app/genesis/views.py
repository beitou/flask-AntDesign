

from flask import request
from flask import jsonify

from app.utils import visited_record
from app.genesis.service import Service

from app.genesis import genesis


@genesis.route('/genesis/api/v1/leads', strict_slashes=False)
def api_v1_leads():
    data = request.values.to_dict()
    visited_record(request)

    try:
        service = Service()
        result = service.leads(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': result
        })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': str(error),
            'data': data
        })


@genesis.route('/genesis/api/v1/create_leads/', strict_slashes=False, methods=['POST'])
def api_v1_create_leads():
    data = request.get_json()

    visited_record(request)

    if 'id' not in data or not data['id']:
        return jsonify({
        'status': 400,
        'message': "invalid parameter 'id'!",
        'data': data
    })

    if 'token' not in data or not data['token']:
        return jsonify({
        'status': 400,
        'message': "invalid parameter 'token'!",
        'data': data
    })

    try:
        service = Service()
        result = service.create_leads(data)
        if 'status' in result:
            return jsonify({
                'status': int(result['status']),
                'message': result['message'],
                'data': result['data']
            })
        else:
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': result
            })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': str(error),
            'data': data
        })


@genesis.route('/genesis/api/v1/search', strict_slashes=False)
def api_v1_search():
    data = request.values.to_dict()
    visited_record(request)

    if 'database' not in data or not data['database']:
        return jsonify({
        'status': 400,
        'message': "invalid parameter 'database'!",
        'data': data
    })

    if 'table' not in data or not data['table']:
        return jsonify({
        'status': 400,
        'message': "invalid parameter 'table'!",
        'data': data
    })

    if 'fields' not in data or not data['fields']:
        data['fields'] = "*"

    try:
        service = Service()
        result = service.search(data)
        total = service.count(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': result,
            'count': total
        })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': str(error),
            'data': data
        })


@genesis.route('/genesis/api/v1/delete', strict_slashes=False, methods=['POST'])
def api_v1_delete():
    data = request.get_json()

    try:
        service = Service()
        result = service.delete_by_finish_id(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': result
        })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': str(error),
            'data': data
        })


@genesis.route('/captcha/code', strict_slashes=False, methods=['POST'])
def api_captcha_code():
    data = request.get_json()

    if 'phone' not in data or not data['phone']:
        return jsonify({
            'status': 400,
            'message': "请求必须添加手机号码!",
            'data': data
        })

    try:
        service = Service()
        count, code = service.captcha_code(data)
        # 当验证码不存在时提示！
        if code is None:
            return jsonify({
                'status': 0,
                'message': '您是尊贵的小帮用户[{}]，验证码不存在，请从新发送。'.format(data['phone']),
                'data': data
            })
        # 当验证码存在1次时是新用户，存在多次时是老用户。
        if count > 1:
            return jsonify({
                'status': 0,
                'message': '您是尊贵的小帮老用户，您的验证码是[{}]'.format(code),
                'data': code
            })
        else:
            return jsonify({
                'status': 0,
                'message': '您是尊贵的小帮新用户，您的验证码是[{}]'.format(code),
                'data': code
            })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': str(error),
        })


@genesis.route('/genesis/create/event', strict_slashes=False, methods=['POST'])
def create_event():
    data = request.get_json()

    if 'event' not in data or not data['event']:
        return jsonify({
            'status': 400,
            'message': "请求必须添加事件!",
            'data': data
        })

    if 'event_time' not in data or not data['event_time']:
        return jsonify({
            'status': 400,
            'message': "请求必须添加事件时间!",
            'data': data
        })

    try:
        service = Service()
        service.create_event(data)
        return jsonify({
            'status': 0,
            'message': '搞定了！',
            'data': {}
        })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': str(error),
        })
