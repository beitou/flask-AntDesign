
import json
import datetime

from flask import current_app

from app.debug import debug


class DebugEncoder(json.JSONEncoder):
    def default(self, obj):
        if callable(obj):
            return {'functon': obj.__name__}
        elif isinstance(obj, datetime.timedelta):
            return str(obj)
        else:
            return json.JSONEncoder.default(self, obj)


@debug.route('/debug/api/v1/config')
def debug():
    return json.dumps({
        'status': 0,
        'message': '调试页面',
        'data': dict(current_app.config)
    }, cls=DebugEncoder)
