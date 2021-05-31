#!/usr/bin/env python
# coding: utf-8

from flask import Blueprint

submit = Blueprint('submit', __name__, url_prefix='/api')

# 由于路由和错误页面都定义在submit这个文件里，导入到蓝图中将他们关联起来
# 又因为models,views,service需要导入蓝图submit，防止循环导入，所以放到最后
from app.submit import views
from app.submit import models
from app.submit import service

