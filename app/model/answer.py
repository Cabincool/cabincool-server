from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import INTEGER
from sqlalchemy.sql import func

from .. import db


class Answer(db.Model):
    __tablename__ = 'answer'

    id = Column(INTEGER(10), primary_key=True)
    user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    question_id = Column(ForeignKey('question.id'), nullable=False, index=True)
    time = Column(DateTime(timezone=True), server_default=func.now())
    link = Column(String(191), nullable=False)
    description = Column(String(191), nullable=False)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
