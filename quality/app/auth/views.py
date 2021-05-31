#!/usr/bin/env python
# coding: utf-8
# author: Liu Yue
# e-mail: liuyue@xiaobangtouzi.com
# Pw @ 2019-07-16 15:52
# history:
#     copy -> lichenglong -> 2019/12/05

from datetime import datetime, timedelta
from flask import request, current_app, session
from flask_login import login_user, current_user, logout_user, login_required
from flask_cors import cross_origin
from sqlalchemy.orm.exc import NoResultFound

from app import db
from .models import User
from app.views import BaseView
from app.utils.rbac import Enforcer

import requests

ERROR_USER_NOT_FOUND = "用户不存在。"
ERROR_AD_EXCEPTION = "AD 查询用户异常。"
ERROR_PASSWORD_WRONG = "密码错误。"
ERROR_NOT_AUTHORIZED = "用户未登录。"

class LoginView(BaseView):

    def get(self):
        # NOTE: check auth cookie
        if current_user.is_authenticated:
            return self.jsonify(200, current_user.to_dict())
        return self.jsonify(202, msg=ERROR_NOT_AUTHORIZED), 202

    def login(self, username: str = '', password: str = '', skipPasswordCheck: bool = False, rememberMe: bool = False):
        try:
            user = User.query.filter_by(username=username, deleted=0).one()
        except NoResultFound:
            try:
                user = User.get_user_from_ad(username)
                if not user:
                    current_app.logger.info(
                        "user is not found: {}".format(username)
                    )
                    return self.jsonify(404, msg=ERROR_USER_NOT_FOUND), 404
            except Exception as e:
                current_app.logger.info(
                    "user is not found: {}, Error: {}".format(username, e)
                )
                return self.jsonify(404, msg=ERROR_USER_NOT_FOUND), 404

        if not skipPasswordCheck and not user.check_password(password):
            return self.jsonify(404, msg=ERROR_PASSWORD_WRONG), 404

        cuser = user.to_dict()
        login_user(user, rememberMe)
        session.permanent = True
        current_app.permanent_session_lifetime = timedelta(minutes=600)
        user.last = datetime.now()
        db.session.add(user)
        db.session.commit()

        return self.jsonify(200, cuser)

    def post(self):
        if current_user.is_authenticated:
            return self.jsonify(200, current_user.to_dict())

        data = request.get_json()
        username, password = data.get("username"), data.get("password")
        return self.login(username, password, rememberMe=data.get("remember_me"))


class LoginWorkWxView(LoginView):

    def get(self):
        # NOTE: check auth cookie
        if current_user.is_authenticated:
            return self.jsonify(200, current_user.to_dict())
        _result = requests.get("https://api.xiaobangtouzi.com/admin-user/api/user-info",
                               cookies=request.cookies)
        res_data = _result.json()
        if res_data['status'] != 200:
            msg = res_data['message'] or ERROR_NOT_AUTHORIZED
            return self.jsonify(202, msg=msg), 202
        email = res_data['data']['email']
        if not email:
            return self.jsonify(202, msg="当前用户在 admin-user 无 email 设置，请联系运维"), 202
        username = email.split('@')[0]
        return self.login(username, '', True)


class LogoutView(BaseView):
    decorators = [login_required]

    def get(self):
        if current_user.is_authenticated:
            logout_user()
        return self.jsonify(200, msg="user is logout.")


class ChangePwd(BaseView):
    decorators = [login_required]

    def post(self):
        # TODO: 更新 AD 密码 或删除 echo 平台删除用户的权限
        data = request.get_json()
        if not current_user.check_password(data.get("oldPassword")):
            return self.jsonify(202, msg="old password is not matched."), 202
        if data.get("newPassword") != data.get("newPassword2"):
            return self.jsonify(202, msg="new password is not equal."), 202
        current_user.password = data.get("newPassword")
        db.session.add(current_user)
        logout_user()
        return self.jsonify(200)


class CurrentUserAction(BaseView):
    decorators = [login_required]

    def get(self):
        return self.jsonify(200, current_user.to_dict())

    def put(self):
        # NOTE: current user put some data and update the database;
        #       but current user only have the permission of change own tel_num.
        data = str(request.get_json())
        if len(data) != 11:
            return self.jsonify(404), 404
        current_user.tel_num = data
        db.session.add(current_user)
        return self.jsonify(200, current_user.to_dict())


PUBLIC_URLS = [
    '/', '/alert/count', '/alert/silence', '/alert/current_recordings',
    '/alert/recordings'
]


class CurrentUserMenuAction(BaseView):
    decorators = [login_required]

    def get(self):
        return self.jsonify(200, PUBLIC_URLS + current_user.menu_permissions)

class CurrentUserDbAction(BaseView):
    decorators = [login_required]

    def get(self):
        return self.jsonify(200, current_user.db_permissions)

GROUP_NAMES = {
    'g:fndn': '基础服务',
    'g:insu': '保险服务',
    'g:fq': '财商基金'
}
class DbListAction(BaseView):
    decorators = [login_required]
    def get(self):
        enforcer = Enforcer(current_user)
        groups = current_user.filter_permissions('resource:modify')
        res = [{'id': group} for group in groups if group.startswith('db:g:') and group != 'db:g:all']
        for group in res:
            group['name'] = GROUP_NAMES[group['id'][3:]]
            group['resources'] = []
            for resource in enforcer.get_resources_under_resource(group['id']):
                if not resource in group['resources']:
                    group['resources'].append(resource)
        return self.jsonify(200, res)

class ResourceDbListAction(BaseView):
    decorators = [login_required]
    def get(self):
        enforcer = Enforcer(current_user)
        groups = [o for o in enforcer.get_all_resources_under_resource('db:g:all') if o.startswith('db:') and not o.startswith('db:g:')]
        return self.jsonify(200, groups)

class DbAction(BaseView):
    decorators = [login_required]
    def put(self, _id):
        if not current_user.has_permission('resource:modify', _id):
            return self.jsonify(403, '您无权修改此组资源'), 403
        data = request.get_json()
        enforcer = Enforcer(current_user)
        resources = enforcer.get_resources_under_resource(_id)
        should_add = [id for id in data if not id in resources]
        should_delete = [id for id in resources if not id in data]
        for resource in should_add:
            enforcer.add_parent_for_resource(resource, _id)
        for resource in should_delete:
            enforcer.delete_parent_for_resource(resource, _id)
        enforcer.ensure_fresh()
        return self.jsonify(200, enforcer.get_resources_under_resource(_id))
class GroupListAction(BaseView):
    decorators = [login_required]
    def get(self):
        enforcer = Enforcer(current_user)
        groups = current_user.group_permissions
        res = [{'id': group} for group in groups if group.startswith('g:') and group != 'g:all']
        for group in res:
            group['name'] = GROUP_NAMES[group['id']]
            group['members'] = [
                User.query.filter_by(id=user).first().to_dict()
                for user in enforcer.get_users_for_role(group['id'])
            ]
            group['resources'] = []
            for resource in enforcer.get_resources_under_resource('db:' + group['id']):
                if not resource in group['resources']:
                    group['resources'].append(resource)
        return self.jsonify(200, res)

class GroupAction(BaseView):
    decorators = [login_required]
    def put(self, _id):
        data = request.get_json()
        enforcer = Enforcer(current_user)
        if not current_user.has_permission('member:modify', _id):
            return self.jsonify(403, '您无权修改此组成员'), 403
        members = enforcer.get_users_for_role(_id)
        should_add = [id for id in data if not id in members]
        should_delete = [id for id in members if not id in data]
        for member in should_add:
            enforcer.add_role_for_user(member, _id)
        for member in should_delete:
            enforcer.delete_role_for_user(member, _id)
        enforcer.ensure_fresh()
        return self.jsonify(200, enforcer.get_users_for_role(_id))

class InitRbacAction(BaseView):
    decorators = [login_required]
    def get(self):
        result = []
        enforcer = Enforcer(current_user)
        # result.append(enforcer.add_permission_for_user('g:admin', '/um/users', 'menu'))
        result.append(enforcer.add_permission_for_user('g:super_admin', '/um/users','menu'))
        result.append(enforcer.add_permission_for_user('g:admin', '/service/services', 'menu'))
        result.append(enforcer.add_permission_for_user('g:super_admin', '/service/services', 'menu'))
        # result.append(enforcer.add_permission_for_user('g:super_admin', '/db/mysql', 'menu'))

        result.append(enforcer.add_role_for_user('g:sre', 'g:super_admin'))

        for username in ['wangyu', 'liuyue', 'xiekaixiang', 'shanyanlei']:
            user = User.query.filter_by(username=username, deleted=0).one()
            result.append(enforcer.add_role_for_user(user.id, 'g:sre'))

        for username in ['mengxiangyu']:
            user = User.query.filter_by(username=username, deleted=0).one()
            result.append(enforcer.add_role_for_user(user.id, 'g:admin'))
            result.append(enforcer.add_role_for_user(user.id, 'g:fndn'))
            result.append(enforcer.add_role_for_user(user.id, 'g:fndn_admin'))

        for username in ['jiaoqiangsheng']:
            user = User.query.filter_by(username=username, deleted=0).one()
            result.append(enforcer.add_role_for_user(user.id, 'g:admin'))
            result.append(enforcer.add_role_for_user(user.id, 'g:insu'))
            result.append(enforcer.add_role_for_user(user.id, 'g:insu_admin'))

        for username in ['zhourongyu']:
            user = User.query.filter_by(username=username, deleted=0).one()
            result.append(enforcer.add_role_for_user(user.id, 'g:admin'))
            result.append(enforcer.add_role_for_user(user.id, 'g:fq'))
            result.append(enforcer.add_role_for_user(user.id, 'g:fq_admin'))

        for g in ['fndn', 'insu', 'fq']:
            result.append(enforcer.add_permission_for_user('g:{}'.format(g), 'db:g:{}'.format(g), 'db:query'))
            result.append(enforcer.add_permission_for_user('g:{}_admin'.format(g), 'g:{}'.format(g), 'member:modify'))
            # result.append(enforcer.add_permission_for_user('g:{}_admin'.format(g), 'db:g:{}'.format(g), 'resource:modify'))
            result.append(enforcer.add_permission_for_user('g:super_admin', 'db:g:{}'.format(g), 'resource:modify'))

        for username in ['wangdong']:
            user = User.query.filter_by(username=username, deleted=0).one()
            result.append(enforcer.add_role_for_user(user.id, 'g:super_admin'))

        result.append(enforcer.add_permission_for_user('g:super_admin', 'db:g:all', 'db:query'))

        result.append(enforcer.add_parent_for_resource('g:fndn', 'g:all'))
        result.append(enforcer.add_parent_for_resource('g:insu', 'g:all'))
        result.append(enforcer.add_parent_for_resource('g:fq', 'g:all'))
        result.append(enforcer.add_permission_for_user('g:super_admin', 'g:all', 'member:modify'))
        result.append(enforcer.add_permission_for_user('g:super_admin', 'db:g:all', 'resource:modify'))

        result.append(enforcer.add_parent_for_resource('db:flow', 'db:g:all'))
        result.append(enforcer.add_parent_for_resource('db:user_center', 'db:g:all'))
        result.append(enforcer.add_parent_for_resource('db:insurance', 'db:g:all'))
        result.append(enforcer.add_parent_for_resource('db:order_center', 'db:g:all'))
        result.append(enforcer.add_parent_for_resource('db:payment', 'db:g:all'))
        result.append(enforcer.add_parent_for_resource('db:wechat', 'db:g:all'))
        result.append(enforcer.add_parent_for_resource('db:xxl-job', 'db:g:all'))
        result.append(enforcer.add_parent_for_resource('db:supplier', 'db:g:all'))
        result.append(enforcer.add_parent_for_resource('db:community', 'db:g:all'))
        result.append(enforcer.add_parent_for_resource('db:crm', 'db:g:all'))
        result.append(enforcer.add_parent_for_resource('db:dp_tag', 'db:g:all'))
        result.append(enforcer.add_parent_for_resource('db:metis', 'db:g:all'))

        result.append(enforcer.add_parent_for_resource('db:flow', 'db:g:fndn'))
        result.append(enforcer.add_parent_for_resource('db:user_center', 'db:g:fndn'))
        result.append(enforcer.add_parent_for_resource('db:order_center', 'db:g:fndn'))
        result.append(enforcer.add_parent_for_resource('db:payment', 'db:g:fndn'))
        result.append(enforcer.add_parent_for_resource('db:wechat', 'db:g:fndn'))
        result.append(enforcer.add_parent_for_resource('db:xxl-job', 'db:g:fndn'))

        result.append(enforcer.add_parent_for_resource('db:insurance', 'db:g:insu'))
        result.append(enforcer.add_parent_for_resource('db:crm', 'db:g:insu'))

        result.append(enforcer.add_parent_for_resource('db:metis', 'db:g:fq'))

        result.append(enforcer.delete_permission_for_user('g:admin', '/um/users', 'menu'))
        result.append(enforcer.delete_permission_for_user('g:super_admin', '/db/mysql', 'menu'))

        return self.jsonify(200, result)
