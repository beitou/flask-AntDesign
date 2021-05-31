#!/usr/bin/python
# -*- coding: UTF-8 -*-
from app.utils import operation_jira
from apscheduler.schedulers.blocking import BlockingScheduler


class MessageRobot:
    def __init__(self):
        self.scheduler = BlockingScheduler()
        self.jira_info = operation_jira.JiraOperation()

    def job_schedulers(self):  # 调度查询BUG作业
        # print(datetime.now())
        self.scheduler.add_job(self.jira_info.bug_search_schedulers, trigger='interval', seconds=60)
        self.scheduler.start()


robot = MessageRobot()
robot.job_schedulers()
