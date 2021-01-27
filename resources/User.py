import os.path
from flask import request
from flask_restful import Resource
import time
from Model import *
import json
from config import  *
from http_response import *
from util import  *
import hashlib 
users_schema = UserSchema(many=True)
user_schema = UserSchema()
class ChangeUserResource(Resource):
    @staticmethod
    def delete(id):
        uid = request.form.get('user_id')
        if (uid == None or uid.isdigit() == False):
            return {'message': 'user_id (int) is required'}, HTTP_NotAccept['code']
        chech_user = User.query.filter_by(id=uid).first()
        if chech_user == None:
            return {'message': 'Permission denied'}, HTTP_NotAccept['code']
        if chech_user.role != 1:
            return {'message': 'Permission denied'}, HTTP_NotAccept['code']
        try:
            delete_resp = User.query.filter_by(id=id).delete()
            db.session.commit()
            msg = 'Delete photo success'
            return {'message': msg}, HTTP_OK['code']
        except  Exception as err:
            return {'message': str(err)}, HTTP_BadRequest['code']
    @staticmethod
    def get(id):
        users = User.query.filter_by(id=id).first()
        if users == None:
            return {'message': 'Userid found'}, HTTP_NotAccept['code']
        try:
            users = user_schema.dumps(users)
            return {'status': 'success', 'data': json.loads(users[0])}, 200
        except  Exception as err:
            return {'message': str(err)}, HTTP_BadRequest['code']
    @staticmethod
    def post(id):
        uid = request.form.get('user_id')
        fullname = request.form.get('fullname')
        password = request.form.get('password')
        email = request.form.get('email')
        role = request.form.get('role')
        users = User.query.filter_by(id=id).first()
        if uid == None:
            return {'message': 'User_id (int) is required'}, HTTP_NotAccept['code']
        if users == None:
            return {'message': 'Userid found'}, HTTP_NotAccept['code']
        if (fullname == None or fullname == ''):
            return {'message': 'fullname is required'}, HTTP_NotAccept['code']
        if (email == None or email == ''):
            return {'message': 'email is required'}, HTTP_NotAccept['code']
        if (role == None or role.isdigit() == False):
            return {'message': 'role (int) is required'}, HTTP_NotAccept['code']
        # Permisision
        if uid != str(id):
            # Check admin
            check_admin_user = User.query.filter_by(id=uid).first()
            if check_admin_user == None:
                return {'message': 'Permision denied'}, HTTP_NotAccept['code']
            if check_admin_user.role != 1:
                return {'message': 'Permision denied'}, HTTP_NotAccept['code']
        try:
            users.fullname = fullname
            if (password!= None or password != ''):
                password = result = hashlib.md5(password.encode("utf-8")).hexdigest()
                users.password = password
            users.email = email
            users.role = role
            db.session.commit()
            return {'message':' Update user success'}, HTTP_OK['code']
        except  Exception as err:
            return {'message': str(err)}, HTTP_BadRequest['code']
class UserResource(Resource):
    @staticmethod
    def get():
        # Need permision
        users = User.query.all()
        users = users_schema.dumps(users)
        return {'status': 'success', 'data': json.loads(users[0])}, 200
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
            password = result = hashlib.md5(password.encode("utf-8")).hexdigest()
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
