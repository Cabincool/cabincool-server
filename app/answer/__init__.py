from flask import Blueprint, Response, request, make_response, jsonify
from flask_restplus import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_claims
from sqlalchemy.sql import func
import json
from app.model.answer import Answer
from app.model.vote import Vote
from sqlalchemy import and_
from app import db

blueprint = Blueprint('answers', __name__)
api = Api(blueprint)


@api.route('/questions/<question_id>/answers')
class Answers(Resource):
    def get(self, question_id):
        answers = Answer.query.filter(Answer.question_id == question_id).all()
        data = []
        for answer in answers:
            data.append(answer.id)
        return Response(json.dumps(data), status=200)

    @jwt_required
    def post(self, question_id):
        content = request.json
        link = content['link']

        claims = get_jwt_claims()
        uid = claims['uid']

        answer = Answer(user_id=uid, question_id=question_id, link=link)
        db.session.add(answer)
        db.session.commit()
        return Response('', status=200)


@api.route('/questions/<question_id>/answers/<answer_id>')
class TheAnswer(Resource):
    def get(self, question_id, answer_id):
        answer = Answer.query.filter(
            and_(Answer.id == answer_id, Answer.question_id == question_id)).first()
        return Response(json.dumps(answer.as_dict()), status=200)

    @jwt_required
    def put(self, question_id, answer_id):
        content = request.json
        link = content['link']

        claims = get_jwt_claims()
        uid = claims['uid']

        answer = Answer.query.filter(
            and_(Answer.user_id == uid, Answer.id == answer_id, Answer.question_id == question_id)).first()
        if answer:
            answer.link = link
            db.session.commit()
            return Response(json.dumps(answer.as_dict()), status=200)
        else:
            return Response('', status=404)

    @jwt_required
    def delete(self, question_id, answer_id):
        try:
            claims = get_jwt_claims()
            uid = claims['uid']
            answer = Answer.query.filter(
                and_(Answer.user_id == uid, Answer.id == answer_id, Answer.question_id == question_id)).first()
            db.session.delete(answer)
            db.session.commit()
            return Response('', status=200)
        except Exception as e:
            print(e)
            return Response('', status=400)


@api.route('/questions/<question_id>/answers/<answer_id>/vote')
class Vote(Resource):
    def get(self, question_id, answer_id):
        vote = Vote.query.filter(
            and_(Vote.question_id == question_id, Vote.answer_id == answer_id))
        total_star = Vote.query.with_entities(
            func.sum(vote.vote_star)).scalar()
        return Response(jsonify(total_star=total_star), 200)

    @jwt_required
    def post(self, question_id, answer_id):
        content = request.json
        vote_star = content['voteStar']

        claims = get_jwt_claims()
        uid = claims['uid']

        vote = Vote(user_id=uid, question_id=question_id,
                    answer_id=answer_id, vote_star=vote_star)
        db.session.commit()
        vote = Vote.query.filter(
            and_(Vote.question_id == question_id, Vote.answer_id == answer_id))
        total_star = Vote.query.with_entities(
            func.sum(vote.vote_star)).scalar()
        return Response(jsonify(count=total_star), 200)
