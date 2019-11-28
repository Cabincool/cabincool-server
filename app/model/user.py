from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.mysql import INTEGER
from .. import db


class User(db.Model):
    __tablename__ = 'user'

    id = Column(INTEGER(10), primary_key=True)
    email = Column(String(191), nullable=False)
    username = Column(String(191), nullable=False)

    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}