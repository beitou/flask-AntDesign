# 新的定时任务只需要去app.config中进行配置

from flask_apscheduler import APScheduler

# 在这进行APScheduler的实例化,避免循环引用问题
quality_apscheduler = APScheduler()
