
from flask import request
from flask import jsonify

from app.treasure.service import Service
from app.treasure import treasure


@treasure.route('/treasure/api/v1/create/', strict_slashes=False, methods=['POST'])
def api_v1_create():
    data = request.get_json()

    # app名称，分支，commit_id，版本类型，打包人，打包时间，下载链接
    if 'name' not in data or not data['name']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter "name"',
            'data': data
        })

    if 'version' not in data or not isinstance(data['version'], int):
        return jsonify({
            'status': 400,
            'message': 'invalid parameter "version"',
            'data': data
        })

    if 'version_name' not in data or not data['version_name']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter "version_name"',
            'data': data
        })

    if 'branch' not in data or not data['branch']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter "branch"',
            'data': data
        })

    if 'platform' not in data or not data['platform']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter "platform"',
            'data': data
        })

    if 'commit_id' not in data or not data['commit_id']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter "commit_id"',
            'data': data
        })

    if 'type' not in data or not data['type']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter "type"',
            'data': data
        })

    if 'submitter' not in data or not data['submitter']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter "submitter"',
            'data': data
        })

    if 'url' not in data or not data['url']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter "url"',
            'data': data
        })

    try:
        service = Service()
        result = service.create(data)
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


@treasure.route('/treasure/app/search/', strict_slashes=False, methods=['GET'])
def app_search():
    data = request.values.to_dict()

    service = Service()
    count, result = service.search(data)
    return jsonify({
        'status': 0,
        'message': 'ok',
        'total': count,
        'data': result,
    })
