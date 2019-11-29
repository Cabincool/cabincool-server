from flask import Blueprint, Response, jsonify, make_response, request
from flask_jwt_extended import create_access_token, get_jwt_identity, get_jwt_claims, jwt_required
from flask_restplus import Api, Resource
import json

from app import db
from app.model.user import User

from firebase_admin import auth

blueprint = Blueprint('users', __name__)
api = Api(blueprint)

# 登入
@api.route('/login')
class Login(Resource):
    def post(self):
        content = request.json
        id_token = content['idToken']
        decoded_token = auth.verify_id_token(id_token)
        uid = decoded_token['uid']
        firebase_user = auth.get_user(uid)

        if firebase_user:
            user = User.query.filter(User.id == uid).first()
            access_token = create_access_token(identity=uid)
            data = {'access_token': access_token}
            if not user:
                new_user = User(email=firebase_user.email,
                                username=firebase_user.display_name)
                db.session.add(new_user)
                db.session.commit()
                make_response(jsonify(data), 200)
            else:
                return make_response(jsonify(data), 200)
        else:
            return Response('', status=401)


@api.route('/users/info')
class Users(Resource):
    @jwt_required
    def get(self):
        claims = get_jwt_claims()
        uid = claims['uid']
        user = User.query.filter(User.id == uid).first()
        return Response(json.dumps(user.as_dict()), status=200)
