
from app import db
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime


class Analysis(db.Model):
    __tablename__ = "tbl_analysis_data"

    id = Column(String(32), primary_key=True, comment="jira id")
    department = Column(String(32), nullable=False, comment="部门")
    summary = Column(String(256), nullable=False, comment="标题")
    priority = Column(String(8), nullable=False, comment="缺陷等级")
    classify = Column(String(16), nullable=False, comment="缺陷类型")
    status = Column(String(8), nullable=False, comment="缺陷状态")
    reason = Column(String(16), nullable=False, comment="原因分类")
    created = Column(DateTime, nullable=False, comment="创建时间")
    updated = Column(DateTime, nullable=False, comment="更新时间")
    reporter_name = Column(String(64), nullable=False, comment="报告人拼音")
    reporter_display_name = Column(String(8), nullable=False, comment="报告人中文")
    assignee_name = Column(String(64), nullable=False, comment="经办人拼音")
    assignee_display_name = Column(String(8), nullable=False, comment="经办人中文")
    url = Column(String(64), nullable=False, comment="jira卡片地址")
    year = Column(String(4), nullable=False, comment="年")
    month = Column(String(2), nullable=False, comment="月")


class Code(db.Model):
    __tablename__ = "tbl_code_data"

    commit_id = Column(String(40), primary_key=True, comment="commit id")
    namespace = Column(String(32), nullable=False, comment="git namespace")
    project = Column(String(64), nullable=False, comment="git project")
    branch = Column(String(32), nullable=False, comment="git branch")
    created = Column(DateTime, nullable=False, comment="创建时间")
    committer = Column(String(64), nullable=False, comment="git commiter")
    committer_email = Column(String(64), nullable=False, comment="commiter email")
    committed_date = Column(DateTime, nullable=False, comment="commiter date")
    additions = Column(Integer, nullable=False, comment="代码增加行数")
    deletions = Column(Integer, nullable=False, comment="代码增加行数")
    total = Column(Integer, nullable=False, comment="代码增加行数")
    status = Column(String(8), nullable=False, comment="代码提交状态")
    year = Column(String(4), nullable=False, comment="年")
    month = Column(String(2), nullable=False, comment="月")


if __name__ == '__main__':
    from app import app
    db.create_all(app=app)
