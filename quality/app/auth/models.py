#!/usr/bin/env python
# coding: utf-8
# author: Liu Yue
# e-mail: liuyue@xiaobangtouzi.com
# Pw @ 2019-07-16 15:52
# history:
#     copy -> lichenglong -> 2019/12/05

from app import login_manager, db
from app.user.models import User
from app.utils.rbac import EMPTY_STRING_MD5
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user

class CasbinLog(db.Model):
    __tablename__ = "casbin_log"

    id = db.Column(db.Integer, primary_key=True)
    create_at = db.Column(db.DateTime, default=datetime.now)
    create_by = db.Column(db.String(16))
    username = db.Column(db.String(64))
    action = db.Column(db.String(16)) # add or remove
    rule = db.Column(db.String(2048))
    version = db.Column(db.String(32))

    @classmethod
    def latest_version(cls):
        first = db.session.query(cls.version).order_by(cls.id.desc()).first()
        return first.version if first else EMPTY_STRING_MD5

    @classmethod
    def add(cls, user: User, action: str, rule: str, version: str):
        log = cls()
        log.create_by = user.id
        log.username = user.username
        log.action = action
        log.rule = rule
        log.version = version
        db.session.add(log)
        db.session.commit()
