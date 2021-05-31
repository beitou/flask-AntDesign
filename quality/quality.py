#!/usr/bin/env python
# coding: utf-8

from flask_cors import CORS
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from werkzeug.utils import import_string
from app import app, db
# orm的模型类需要导入
from app.submit.models import SubmitData,TestReportData,CostTimeData

# 兼容时临时处理，线上版本可用后让大家迁移。
from flask import request
from flask import jsonify
from app.treasure.service import Service


@app.route('/treasure/api/v1/create/', strict_slashes=False, methods=['POST'])
def api_v1_create():
    data = request.get_json()
    print(data)

    # app名称，分支，commit_id，版本类型，打包人，打包时间，下载链接
    if 'name' not in data or not data['name']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter "name"',
            'data': data
        })

    if 'version' not in data or not data['version']:
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

    if 'created' not in data or not data['created']:
        return jsonify({
            'status': 400,
            'message': 'invalid parameter "created"',
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
# 兼容时临时处理结束


CORS(app, supports_credentials=True)

# 这里后续可以放到配置文件中，每次增加一个模块增加一个配置即可。
blueprints = [
    'app.analysis:analysis',
    'app.genesis:genesis',
    'app.project:project',
    'app.submit:submit',
    'app.treasure:treasure',
    'app.user:user',
    'app.debug:debug'
]

# 新增子app，需要注册蓝图
for bp_name in blueprints:
    bp = import_string(bp_name)
    app.register_blueprint(bp)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


def make_shell_context():
    return dict(app=app, db=db)


manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

# 在调试模式下，Flask的重新加载器将加载烧瓶应用程序两次。
# 因此flask总共有两个进程. 重新加载器监视文件系统的更改并在不同的进程中启动真实应用程序
if __name__ == '__main__':
    manager.run()
