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
class PermisionForPhotoResource(Resource):
    @staticmethod
    def post():
      own_user_id = request.form.get('own_user_id')
      user_id = request.form.get('user_id')
      photo_id = request.form.get('photo_id')
      permission = request.form.get('permission')
      if (str(own_user_id) != str(user_id)):
            return {'message': 'User is the same'}, HTTP_Forbidden['code']
      if (own_user_id == None or own_user_id.isdigit() == False):
            return {'message': 'own_user_id (int) is required'}, HTTP_NotAccept['code']
      if (permission == None or permission.isdigit() == False or str(permission) != '1' or str(permission) != '2'):
            return {'message': 'permission required 1 or 2'}, HTTP_NotAccept['code']
      if (user_id == None or user_id.isdigit() == False):
            return {'message': 'user_id (int) is required'}, HTTP_NotAccept['code']
      if (photo_id == None or photo_id.isdigit() == False):
            return {'message': 'photo_id (int) is required'}, HTTP_NotAccept['code']
      chech_own = User.query.filter_by(id=own_user_id).first()
      if (chech_own):
            return {'message': 'Not found own user'}, HTTP_NotFound['code']
      chech_user = User.query.filter_by(id=user_id).first()
      if (chech_user):
            return {'message': 'Not found user'}, HTTP_NotFound['code']
      chech_photo = Photo.query.filter_by(id=photo_id).first()
      if (chech_photo):
            return {'message': 'Not found photo'}, HTTP_NotFound['code']
        # check existed permission 
      try:
            if (str(chech_own.id) != str(chech_photo.user_id)):
                return {'message': 'User is not own photo'}, HTTP_NotFound['code']
            check_exist_permission = PermissionForPhoto.query.filter_by(id_user=user_id, id_Photo=photo_id).first()
            if (check_exist_permission != None):
                check_exist_permission.permision = permission
            else:
                permission = PermissionForPhoto(
                    id_user= user_id,
                    id_Photo= photo_id,
                    permision=permission
                )
                db.session.add(permission)
            db.session.commit()
            return {'message': 'Set permission success'}, HTTP_OK['code']
      except Exception as err:
            return {'message': str(err)}, HTTP_Forbidden['code']

class PermisionForAlbumResource(Resource):
    @staticmethod
    def post():
      own_user_id = request.form.get('own_user_id')
      user_id = request.form.get('user_id')
      album_id = request.form.get('album_id')
      permission = request.form.get('permission')
      if (str(own_user_id) != str(user_id)):
            return {'message': 'User is the same'}, HTTP_Forbidden['code']
      if (own_user_id == None or own_user_id.isdigit() == False):
            return {'message': 'own_user_id (int) is required'}, HTTP_NotAccept['code']
      if (permission == None or permission.isdigit() == False or str(permission) != '1' or str(permission) != '2'):
            return {'message': 'permission required 1 or 2'}, HTTP_NotAccept['code']
      if (user_id == None or user_id.isdigit() == False):
            return {'message': 'user_id (int) is required'}, HTTP_NotAccept['code']
      if (album_id == None or album_id.isdigit() == False):
            return {'message': 'photo_id (int) is required'}, HTTP_NotAccept['code']
      chech_own = User.query.filter_by(id=own_user_id).first()
      if (chech_own):
            return {'message': 'Not found own user'}, HTTP_NotFound['code']
      chech_user = User.query.filter_by(id=user_id).first()
      if (chech_user):
            return {'message': 'Not found user'}, HTTP_NotFound['code']
      chech_photo = Album.query.filter_by(id=album_id).first()
      if (chech_photo):
            return {'message': 'Not found photo'}, HTTP_NotFound['code']
        # check existed permission 
      try:
            if (str(chech_own.id) != str(chech_photo.user_id)):
                return {'message': 'User is not own photo'}, HTTP_NotFound['code']
            check_exist_permission = PermissionForAlbum.query.filter_by(id_user=user_id, id_album=album_id).first()
            if (check_exist_permission != None):
                check_exist_permission.permision = permission
            else:
                permission = PermissionForAlbum(
                    id_user= user_id,
                    id_album= album_id,
                    permision=permission
                )
                db.session.add(permission)
            db.session.commit()
            return {'message': 'Set permission success'}, HTTP_OK['code']
      except Exception as err:
            return {'message': str(err)}, HTTP_Forbidden['code']