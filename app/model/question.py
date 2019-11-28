from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.sql import func

from .. import db


class Question(db.Model):
    __tablename__ = 'question'

    id = Column(INTEGER(10), primary_key=True)
    title = Column(String(191), nullable=False)
    time = Column(DateTime(timezone=True), server_default=func.now())
    description = Column(String(191), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}