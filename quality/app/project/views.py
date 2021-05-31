

from flask import request
from flask import jsonify
from flask import Blueprint
from flask import render_template

from app.project.service import Service

from app.project import project


@project.route('/project/search', strict_slashes=False)
def search():
    data = request.values.to_dict()

    try:
        service = Service()
        result = service.search(data)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': result
        })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': str(error),
            'data': {}
        })
