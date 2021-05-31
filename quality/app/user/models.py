
from flask_login import UserMixin

from app import db


class User(UserMixin, db.Model):

    __tablename__ = 'tb_user'

    id = db.Column(db.String(120), primary_key=True, index=True, unique=True)
    name = db.Column(db.String(64), index=True, unique=True)
    display_name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    department = db.Column(db.String(120), index=True, unique=True)
    mobile = db.Column(db.String(11), index=True, unique=True)
    title = db.Column(db.String(64), index=True, unique=True)
    role = db.Column(db.String(64), index=True, unique=True)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


if __name__ == '__main__':
    user = User()
    user.id = 1
    user.name = "dahuaimao"
    user.display_name = "大坏猫"
    user.email = "dahuaimao@xiaobangtouzi.com"
    user.department = "抓老鼠部门"
    user.mobile = "13800138000"
    user.title = "黑猫警长"
    user.role = "公务员"
    print(user.to_dict())
