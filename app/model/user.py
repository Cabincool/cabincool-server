from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.mysql import INTEGER, CHAR
from .. import db


class User(db.Model):
    __tablename__ = 'user'

    id = Column(INTEGER(10), primary_key=True)
    uid = Column(CHAR(32), nullable=False,  unique=True)
    email = Column(String(191), nullable=False)
    username = Column(String(191), nullable=False)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}
