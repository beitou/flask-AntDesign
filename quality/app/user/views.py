import datetime
import traceback

from flask import request
from flask import jsonify
from flask import session
from flask import current_app

from flask_login import login_user
from flask_login import logout_user
from flask_login import current_user
from flask_login import login_required

import requests

from app.user import user
from app.user.service import UserService
from app.user.service import LoginService

from app import login_manager


@login_manager.user_loader
def load_user(userid):
    return query_user(userid)


def query_user(name):
    """
    # 这里要求返回用户或None。
    :param user_id:
    :return:
    """
    service = LoginService()
    return service.get_user_from_ldap(name)


@user.route("/login/", methods=['GET', 'POST'])
def login():
    """
    # 先查询用户是否存在，存在则校验密码。
    :return:
    """
    try:
        if current_user.is_authenticated:
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': {
                    'displayName': '李成龙',
                    'name': 'lichenglong',
                }
                # 'data': current_user.to_dict()
            })

        if request.method == 'GET':
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': current_user.to_dict()
            })

        if request.method == 'POST':
            data = request.get_json()
            user = query_user(data['username'])
            if not user:
                return jsonify({
                    'status': 400,
                    'message': '用户名不存在，请输入正确的用户名！',
                    'data': data
                })

            service = LoginService()
            login = service.check_password(data['password'], user)
            if not login:
                return jsonify({
                    'status': 400,
                    'message': '密码不正确，请输入正确的密码！',
                    'data': data
                })

            # 通过Flask-Login的login_user方法登录用户
            login_user(user)
            login_user(user, True)
            session.permanent = True
            current_app.permanent_session_lifetime = datetime.timedelta(minutes=600)
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': user.to_dict()
            })
    except Exception as error:
        return jsonify({
            'status': 500,
            'message': str(error),
            'trace': traceback.format_stack()
        })


@user.route("/login_workwx/")
def workwx():
    # NOTE: check auth cookie
    try:
        if current_user.is_authenticated:
            return jsonify({
                'status': 0,
                'message': 'ok',
                'data': current_user.to_dict()
            })

        _result = requests.get("https://api.xiaobangtouzi.com/admin-user/api/user-info",
                             cookies=request.cookies)
        res_data = _result.json()

        if res_data['status'] != 200:
            return res_data

        email = res_data['data']['email']
        if not email:
            return jsonify({
                'status': 203,
                'message': "当前用户在 admin-user 无 email 设置，请联系运维",
                'data': {}
            })

        username = email.split('@')[0]
        user = query_user(username)

        if not user:
          return jsonify({
            'status': 400,
            'message': '用户名不存在，请输入正确的用户名！',
            'data': res_data
          })

        # 通过Flask-Login的login_user方法登录用户
        login_user(user, True)
        session.permanent = True
        current_app.permanent_session_lifetime = datetime.timedelta(minutes=600)
        return jsonify({
          'status': 0,
          'message': 'ok',
          'data': user.to_dict()
        })

    except Exception as error:
        return jsonify({
            'status': 500,
            'message': "当获取登陆状态时出错，请联系管理员！",
            'error': str(error),
            'trace': traceback.format_stack()
        })


@login_required
@user.route("/logout/")
def logout():
    logout_user()
    user = current_user.to_dict()
    return jsonify({
        'status': 0,
        'message': str(user['user_id']),
        'data': user
    })


@user.route('/user/search/')
def user_search():
    data = request.values.to_dict()

    try:
        key = data.get('key', None)
        value = data.get('value', None)
        department = int(data.get('department', 3))

        service = UserService()
        users = service.search_user(key, value, department)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': users,
        })
    except Exception:
        return jsonify({
            'status': 500,
            'message': '获取用户列表失败，请联系管理员！',
            'data': data,
        })


@user.route('/user/role/')
def user_role():
    data = request.values.to_dict()

    try:
        role = data.get('role', None)

        service = UserService()
        users = service.search_role(role)
        return jsonify({
            'status': 0,
            'message': 'ok',
            'data': users,
        })
    except Exception:
        return jsonify({
            'status': 500,
            'message': '获取用户列表失败，请联系管理员！',
            'data': data,
        })
