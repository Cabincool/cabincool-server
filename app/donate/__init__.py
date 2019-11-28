from flask import Blueprint, Response, request
from flask_restplus import Api, Resource
from flask_jwt_extended import jwt_required, get_jwt_claims
import json
from app.model.donate import Donate

from app import db

blueprint = Blueprint('questions', __name__)
api = Api(blueprint)


@api.route('')
class Donates(Resource):
    def get(self):
        donates = Donate.query.all()
        data = []
        for donate in donates:
            data.append(donate.id)
        return Response(json.dumps(data), status=200)

    def post(self):
        money = request.form['money']
        # starCount = request.form['starCount']
        # basicStar = request.form['basicStar']
        donate = Donate(money=money)
        db.session.add(donate)
        db.session.commit()
        return Response('', status=200)


@api.route('/<id>')
class TheQuestion(Resource):
    def get(self, id):
        donate = Donate.query.filter(Donate.id == id).first()
        return Response(json.dumps(donate.as_dict()), status=200)