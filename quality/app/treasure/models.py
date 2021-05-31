
import datetime

from app import db
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from app.models import BaseModel


class Treasure(BaseModel):
    __tablename__ = "tbl_treasure_data"

    id = Column(Integer, primary_key=True, comment="ID")
    name = Column(String(32), nullable=False, comment="App名称")
    version_name = Column(String(32), nullable=False, comment="App版本名")
    version = Column(String(32), nullable=False, comment="App版本")
    branch = Column(String(32), nullable=False, comment="分支名")
    platform = Column(String(32), nullable=False, comment="平台[iOS|Android]")
    type = Column(String(32), nullable=False, comment="分支名")
    commit_id = Column(String(40), nullable=False, comment="commit id")
    submitter = Column(String(32), nullable=False, comment="分支名")
    url = Column(String(2048), nullable=False, comment="下载链接")
    image = Column(String(2048), nullable=False, comment="二维码图片地址")
    created = Column(DateTime, default=datetime.datetime.now, comment="创建时间")


if __name__ == '__main__':
    from app import app
    db.create_all(app=app)
