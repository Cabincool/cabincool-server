from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.mysql import INTEGER
from .. import db


class Vote(db.Model):
    __tablename__ = 'vote'

    id = Column(INTEGER(10), primary_key=True)
    user_id = Column(ForeignKey('user.id'), nullable=False, index=True)
    question_id = Column(ForeignKey('question.id'), nullable=False, index=True)
    answer_id = Column(ForeignKey('answer.id'), nullable=False)
    vote_star = Column(INTEGER(191), nullable=False)


    def as_dict(self):
        return {c.name: str(getattr(self, c.name)) for c in self.__table__.columns}