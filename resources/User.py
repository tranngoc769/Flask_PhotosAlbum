import os.path
from flask import request
from flask_restful import Resource
import time
from Model import *
import json
from config import  *
from http_response import *
from util import  *
users_schema = UserSchema(many=True)
user_schema = UserSchema()
class UserResource(Resource):
    @staticmethod
    def get():
        users = User.query.all()
        users = users_schema.dumps(users)
        return {'status': 'success', 'data': users}, 200
    @staticmethod
    def post():
        username = request.form.get('username')
        fullname = request.form.get('fullname')
        password = request.form.get('password')
        email = request.form.get('email')
        role = request.form.get('role')
        # VALIDATE
        if (username == None or username == ''):
            return {'message': 'username is required'}, HTTP_NotAccept['code']
        if (fullname == None or fullname == ''):
            return {'message': 'fullname is required'}, HTTP_NotAccept['code']
        if (password == None or password == ''):
            return {'message': 'password is required'}, HTTP_NotAccept['code']
        if (email == None or email == ''):
            return {'message': 'email is required'}, HTTP_NotAccept['code']
        if (role == None or role.isdigit() == False):
            return {'message': 'role (int) is required'}, HTTP_NotAccept['code']
        chech_user = User.query.filter_by(username=username,email=email).first()
        if (chech_user):
            return {'message': 'username / email existed :'+str(username)}, 403
        # END VALIDATE
        # CREATE DIR FOR ALBUM
        try:
            # PREPARE INFORMATION
            date_created = get_current_time()
            # CREATE USER
            user = User(
                username=username,
                fullname= fullname,
                password= password,
                email= email,
                date_created=date_created,
                role= role
                )
            # SAVE TO DB
            db.session.add(user)
            db.session.commit()
            result = user_schema.dump(user)
            return {"status": 'success', 'data': result[0]}, 200
        except Exception as err:
            return {'message': str(err)}, HTTP_Forbidden['code']
