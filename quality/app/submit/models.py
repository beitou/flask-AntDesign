#!/usr/bin/env python
# coding: utf-8

import datetime
import time

from sqlalchemy.orm import relationship
from app import db
from app.config import TEAM_DICT

# 不使用外键
class SubmitData(db.Model):
    __tablename__ = "tbl_submit_data"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(100),nullable=False,default='quality')
    version = db.Column(db.String(100),nullable=False,default='quality')
    pm_name = db.Column(db.String(100),nullable=False,default='quality')
    pm_mail = db.Column(db.String(100),nullable=False,default='quality')
    fe_name = db.Column(db.String(100),nullable=False,default='quality')
    fe_mail = db.Column(db.String(100),nullable=False,default='quality')
    rd_name = db.Column(db.String(100),nullable=False,default='quality')
    rd_mail = db.Column(db.String(100),nullable=False,default='quality')
    submiter_name = db.Column(db.String(100),nullable=False,default='quality')
    submiter_mail = db.Column(db.String(100),nullable=False,default='quality')
    qa_name = db.Column(db.String(100),nullable=False,default='quality')
    qa_mail = db.Column(db.String(100),nullable=False,default='quality')
    prd = db.Column(db.String(100),nullable=False,default='quality')
    tech = db.Column(db.String(100),nullable=False,default='quality')
    team = db.Column(db.String(100),nullable=False,default='quality')
    sprint = db.Column(db.String(100),nullable=False,default='quality')
    card = db.Column(db.String(100),nullable=False,default='quality') # 需求卡片
    group = db.Column(db.String(100),nullable=False,default='quality')
    repository = db.Column(db.String(100),nullable=False,default='quality')
    branch = db.Column(db.String(100),nullable=False,default='quality')
    host = db.Column(db.String(100),nullable=False,default='quality')
    selftest = db.Column(db.Boolean,nullable=False,default=False)
    testcase = db.Column(db.String(1024),nullable=False,default='quality')
    smoke = db.Column(db.String(100),nullable=False,default='quality')
    influence = db.Column(db.String(1024),nullable=False,default='quality')
    fe_start = db.Column(db.String(100),nullable=False,default='quality')
    fe_end = db.Column(db.String(100),nullable=False,default='quality')
    rd_start = db.Column(db.String(100),nullable=False,default='quality')
    rd_end = db.Column(db.String(100),nullable=False,default='quality')
    cc_recs = db.Column(db.String(100),nullable=False,default='quality')
    sub_mail_recs = db.Column(db.String(1024),nullable=False,default='quality')
    submit_status = db.Column(db.String(100),nullable=False,default='quality') # wait:待测试，qa:qa测试，staging:staging测试，online:已上线,all:全部状态
    create_at = db.Column(db.DateTime,nullable=False,default=datetime.datetime.now)

    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
    __mapper_args__= {
        "order_by":create_at.desc()
    }

    def submitdata_schema(self):
        return {
            'id':self.id,
            'name':self.name,
            'version':self.version,
            'pm_name':self.pm_name,
            'pm_mail': self.pm_mail,
            'fe_name':self.fe_name,
            'fe_mail': self.fe_mail,
            'rd_name': self.rd_name,
            'rd_mail': self.rd_mail,
            'submiter_name':self.submiter_name,
            'submiter_mail': self.submiter_mail,
            'qa_name':self.qa_name,
            'qa_mail': self.qa_mail,
            'prd':self.prd,
            'tech':self.tech,
            'team':TEAM_DICT.get(self.team,u'其他'),
            'sprint':self.sprint,
            'card':self.card,
            'group':self.group,
            'repository':self.repository,
            'branch':self.branch,
            'host':self.host,
            'selftest':self.selftest,
            'testcase':self.testcase,
            'smoke':self.smoke,
            'influence':self.influence,
            'fe_start':self.fe_start,
            'fe_end': self.fe_end,
            'rd_start': self.rd_start,
            'rd_end':self.rd_end,
            'cc_recs':self.cc_recs,
            'sub_mail_recs':self.sub_mail_recs,
            'submit_status':self.submit_status,
            'create_at': self.create_at.strftime("%Y-%m-%d %H:%M:%S")
        }


class TestReportData(db.Model):
    __tablename__ = "tbl_testreport_data"

    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    t_os_name = db.Column(db.String(100),nullable=False,default='quality')
    t_browsers = db.Column(db.String(100),nullable=False,default='quality')
    t_phones = db.Column(db.String(100),nullable=False,default='quality')
    t_link = db.Column(db.String(100),nullable=False,default='quality')
    t_methods = db.Column(db.String(1024),nullable=False,default='quality')
    t_summary = db.Column(db.String(1024),nullable=False,default='quality')
    t_memo = db.Column(db.String(1024),nullable=False,default='quality')
    bug_fatal = db.Column(db.String(100),nullable=False,default='quality')
    bug_serious = db.Column(db.String(100),nullable=False,default='quality')
    bug_general = db.Column(db.String(100),nullable=False,default='quality')
    bug_low = db.Column(db.String(100),nullable=False,default='quality')
    bug_suggest = db.Column(db.String(1024),nullable=False,default='quality')
    bug_new = db.Column(db.String(1024),nullable=False,default='quality')
    bug_processing = db.Column(db.String(1024),nullable=False,default='quality')
    bug_resolve = db.Column(db.String(100),nullable=False,default='quality')
    bug_refuse = db.Column(db.String(1024),nullable=False,default='quality')
    bug_closed = db.Column(db.String(1024),nullable=False,default='quality')
    bug_function = db.Column(db.String(1024),nullable=False,default='quality')
    bug_data = db.Column(db.String(1024),nullable=False,default='quality')
    bug_ui = db.Column(db.String(1024),nullable=False,default='quality')
    bug_compatibility = db.Column(db.String(100),nullable=False,default='quality')
    bug_performance = db.Column(db.String(1024),nullable=False,default='quality')
    bug_security = db.Column(db.String(1024),nullable=False,default='quality')
    t_create_at = db.Column(db.DateTime,nullable=False,default=datetime.datetime.now)
    submit_data_id = db.Column(db.Integer,nullable=False,default=0)
    # submit_data_id = db.Column(db.Integer,db.ForeignKey("tbl_submit_data.id"))
    # submit_data = relationship("SubmitData",backref=db.backref("tbl_testreport_data"))

    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
    __mapper_args__= {
        "order_by":t_create_at.desc()
    }

    def test_report_data_schema(self):
        return {
            'id':self.id,
            't_os_name':self.t_os_name,
            't_browsers':self.t_browsers,
            't_phones':self.t_phones,
            't_link':self.t_link,
            't_methods': self.t_methods,
            't_summary':self.t_summary,
            't_memo':self.t_memo,
            'bug_fatal': self.bug_fatal,
            'bug_serious': self.bug_serious,
            'bug_general': self.bug_general,
            'bug_low': self.bug_low,
            'bug_suggest': self.bug_suggest,
            'bug_new': self.bug_new,
            'bug_processing': self.bug_processing,
            'bug_resolve': self.bug_resolve,
            'bug_refuse': self.bug_refuse,
            'bug_closed': self.bug_closed,
            'bug_function': self.bug_function,
            'bug_data': self.bug_data,
            'bug_ui': self.bug_ui,
            'bug_compatibility': self.bug_compatibility,
            'bug_performance': self.bug_performance,
            'bug_security': self.bug_security,
            'submit_data_id': self.submit_data_id,
            't_create_at': self.t_create_at.strftime("%Y-%m-%d %H:%M:%S")
        }


class CostTimeData(db.Model):
    __tablename__ = "tbl_cost_time_data"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    c_qa_start = db.Column(db.String(100),nullable=False,default='quality')
    c_staging_start = db.Column(db.String(100),nullable=False,default='quality')
    c_online_start = db.Column(db.String(100),nullable=False,default='quality')
    c_qa_count = db.Column(db.Integer,nullable=False,default=0)
    c_dev_time = db.Column(db.String(100),nullable=False,default='quality')
    c_create_at = db.Column(db.DateTime,nullable=False, default=datetime.datetime.now)
    submit_data_id = db.Column(db.Integer,nullable=False,default=0)
    # submit_data_id = db.Column(db.Integer, db.ForeignKey("tbl_submit_data.id"))
    # submit_data = relationship("SubmitData", backref=db.backref("tbl_cost_time_data"))

    __table_args__ = {'mysql_engine': 'InnoDB', 'mysql_charset': 'utf8'}
    __mapper_args__ = {
      "order_by": c_create_at.desc()
    }

    def cost_time_data_schema(self):
        return {
          'id': self.id,
          'c_qa_start': self.c_qa_start,
          'c_staging_start': self.c_staging_start,
          'c_online_start': self.c_online_start,
          'c_qa_count':self.c_qa_count,
          'c_dev_time':self.c_dev_time,
          'submit_data_id': self.submit_data_id,
          'c_create_at': self.c_create_at.strftime("%Y-%m-%d %H:%M:%S")
        }
