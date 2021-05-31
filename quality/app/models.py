
from app import db

class BaseModel(db.Model):
    __abstract__ = True

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
