from flask import Blueprint, Response, request
from flask_restplus import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_claims
import json
from app.model.question import Question

from app import db

blueprint = Blueprint('questions', __name__)
api = Api(blueprint)


@api.route('')
class Questions(Resource):
    def get(self):
        questions = Question.query.all()
        data = []
        for question in questions:
            data.append(question.id)
        return Response(json.dumps(data), status=200)

    @jwt_required
    def post(self):
        title = request.form['title']
        description = request.form['description']
        question = Question(title=title, description=description)
        db.session.add(question)
        db.session.commit()
        return Response('', status=200)


@api.route('/<id>')
class TheQuestion(Resource):
    def get(self, id):
        question = Question.query.filter(Question.id == id).first()
        return Response(json.dumps(question.as_dict()), status=200)

    @jwt_required
    def put(self, id):
        title = request.form['title']
        description = request.form['description']
        question = Question.query.filter(Question.id == id).first()
        if question:
            question.title = title
            question.description = description
            db.session.commit()
            return Response(json.dumps(question.as_dict()), status=200)
        else:
            return Response('', status=404)

    @jwt_required
    def delete(self, id):
        try:
            question = Question.query.filter(Question.id == id).first()
            db.session.delete(question)
            db.session.commit()
            return Response('', status=200)
        except Exception as e:
            print(e)
            return Response('', status=400)

@api.route('/<id>/donate')
class Donate(Resource):
    @jwt_required
    def post(self, id):
        content = request.json
        return Response('', 200)