from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import INTEGER
from .. import db


class Donate(db.Model):
    __tablename__ = 'donate'

    id = Column(INTEGER(10), primary_key=True)
    user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    question_id = Column(ForeignKey('question.id'), nullable=False, index=True)
    starCount = Column(INTEGER(191), nullable=False)
    money = Column(INTEGER(191), nullable=False)
    basicStar = Column(INTEGER(191), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}