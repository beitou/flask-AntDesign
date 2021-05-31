#!/usr/bin/env python
# coding: utf-8
# author: wangyu
# e-mail: wangyu@xiaobangtouzi.com
# Pw @ 2019-11-12 10:56
# history:
#     copy -> lichenglong -> 2019/12/05

import os
import copy
import casbin
from casbin import persist
from casbin.config import Config
from casbin.model import Model
from casbin_sqlalchemy_adapter import CasbinRule, Adapter as SqlalchemyAdapter
from app.config import config
from sqlalchemy import create_engine
import hashlib
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

ENV = os.getenv("FLASK_ENV") or "development"
config = config.get(ENV)

engine = create_engine(config.SQLALCHEMY_DATABASE_URI, pool_recycle=config.SQLALCHEMY_POOL_RECYCLE, echo=config.SQLALCHEMY_ECHO)

text_model = '''[request_definition]
r = sub, obj, act

[policy_definition]
p = sub, obj, act

[role_definition]
g = _, _
g2 = _, _

[policy_effect]
e = some(where (p.eft == allow))

[matchers]
m = g(r.sub, p.sub) && g2(r.obj, p.obj) && r.act == p.act
'''

model = Model()
model.load_model_from_text(text_model)

EMPTY_STRING_MD5 = 'd41d8cd98f00b204e9800998ecf8427e'

class Adapter(SqlalchemyAdapter):
    cached_policy = ''
    current_version = EMPTY_STRING_MD5

    def expire(self):
        self._session.expire_all()
        self._session.commit()
        Adapter.cached_policy = ''
        Adapter.current_version = EMPTY_STRING_MD5

    def load_policy(self, model):
        """loads all policy rules from the storage."""
        cached_policy = ''
        m = hashlib.md5()
        lines = []
        if self.cached_policy != '':
            lines = self.cached_policy.strip().split('\n')
        else:
            lines = [str(line) for line in self._session.query(CasbinRule).all()]
        for policy in lines:
            policy_line = policy + "\n"
            persist.load_policy_line(policy, model)
            cached_policy += policy_line
            m.update(policy_line.encode())

        Adapter.cached_policy = cached_policy
        Adapter.current_version = m.hexdigest()

class Enforcer(casbin.Enforcer):
    def __init__(self, user):
        super().__init__(model, Adapter(engine))
        self.user = user
        self.own_permissions = []
        self.ensure_fresh()
    def log_casbin_change(self, action, rule):
        from app.auth.models import CasbinLog
        self.adapter.expire()
        self.load_policy()
        version = self.adapter.current_version
        CasbinLog.add(self.user, action, rule, version)
    def _add_policy(self, sec, ptype, rule):
        """adds a rule to the current policy."""
        rule_added = super()._add_policy(sec, ptype, rule)
        if rule_added:
            self.log_casbin_change('add', ', '.join([ptype] + rule))
        return rule_added
    def add_parent_for_resource(self, resource: str, resource_parent: str):
        return self._add_policy('g', 'g2', [resource, resource_parent])
    def get_resources_under_resource(self, resource):
        """gets the users that has a role."""
        return self.model.model['g']['g2'].rm.get_users(resource)

    def get_resources_contains_resource(self, resource):
        return self.model.model['g']['g2'].rm.get_roles(resource)


    def get_implicit_roles_for_user(self, user, domain=None):
        checked = []
        roles = self.get_roles_for_user(user)
        res = copy.copy(roles)
        i = 0
        while i < len(res):
            r = res[i]
            if r in checked:
                continue
            _roles = self.get_roles_for_user(r)
            res.extend([role for role in _roles if not role in res])
            i += 1
        return res

    def get_all_resources_contains_resource(self, resource):
        checked = []
        resources = self.get_resources_contains_resource(resource)
        res = copy.copy(resources)
        i = 0
        while i < len(res):
            r = res[i]
            if r in checked:
                continue
            _resources = self.get_resources_contains_resource(r)
            res.extend([rs for rs in _resources if not rs in res])
            i += 1
        return res

    def get_all_resources_under_resource(self, resource):
        checked = []
        resources = self.get_resources_under_resource(resource)
        res = copy.copy(resources)
        i = 0
        while i < len(res):
            r = res[i]
            if r in checked:
                continue
            _resources = self.get_resources_under_resource(r)
            res.extend([rs for rs in _resources if not rs in res])
            i += 1
        return res

    def get_all_implicit_permissions_for_user(self, user, domain=None):
        """
            比 get_implicit_roles_for_user 新增加所有资源下包含的下级资源
        """
        if user == self.user.id and self.own_permissions:
            return self.own_permissions
        permissions = self.get_implicit_permissions_for_user(user)
        res = []
        for p in permissions:
            try:
                ext = [p[0], [p[1]] + self.get_all_resources_under_resource(p[1]), p[2]]
            except:
                pass
            res.append(ext)
        self.own_permissions = res
        return res



    def _remove_policy(self, sec, ptype, rule):
        """removes a rule from the current policy."""
        rule_removed = super()._remove_policy(sec, ptype, rule)
        if rule_removed:
            self.log_casbin_change('remove', ', '.join([ptype] + rule))
        return rule_removed
    def delete_parent_for_resource(self, resource, parent_resource):
        return self.remove_named_grouping_policy('g2', resource, parent_resource)
    def _remove_filtered_policy(self, sec, ptype, field_index, *field_values):
        """removes rules based on field filters from the current policy.
        disabled here"""
        raise Exception("not supported here, please remove policy one by one")

    def has_permission(self, user, action, resource=None):
        permissions = self.get_all_implicit_permissions_for_user(user)
        # print(permissions)
        return any(p[2] == action and (resource == None or resource in p[1]) for p in permissions)

    def filter_permissions(self, user, action):
        permissions = self.get_all_implicit_permissions_for_user(user)
        res = []
        for p in permissions:
            if p[2] != action:
                continue
            for pn in p[1]:
                if not pn in res:
                    res.append(pn)
        return res


    def latest_version(self):
        from app.auth.models import CasbinLog
        return CasbinLog.latest_version()
    def refresh_policy(self):
        self.adapter.expire()
        self.load_policy()
        self.own_permissions = self.get_all_implicit_permissions_for_user(self.user.id)
    def ensure_fresh(self):
        latest_version = self.latest_version()
        current_version = self.adapter.current_version
        if latest_version != current_version:
            self.refresh_policy()
