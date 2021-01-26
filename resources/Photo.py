import os.path
from flask import request
from flask_restful import Resource
import time
from Model import *
import json
from config import  *
from http_response import *
from util import  *
photos_schema = PhotoSchema(many=True)
photo_schema = PhotoSchema()

class DeletePhotoResource(Resource):
    @staticmethod
    def post(photoid):
        # Delete
        check_photos = Photo.query.filter_by(id=photoid).first()
        if (check_photos== None):
            return {'message': 'Not found photo id : ' + str(photoid)}, HTTP_NotFound['code']
        try:
            path = check_photos.path
            delete_resp = Photo.query.filter_by(id=photoid).delete()
            db.session.commit()
            msg = 'Delete photo success'
            try:
                os.remove(path)
            except Exception as rm_err:
                msg = msg + ", "+str(rm_err)
            return {'message': msg}, HTTP_OK['code']
        except  Exception as err:
            return {'message': str(err)}, HTTP_BadRequest['code']
        return {'message': 'Delete photo success'}, HTTP_OK['code']
class PhotoResource(Resource):
    @staticmethod
    def get(id):
        photos = Photo.query.all()
        photos = photos_schema.dumps(photos)
        return {'status': 'success', 'data': photos}, 200
    @staticmethod
    def post():
        if (len(request.files)==0):
            return {'message': 'Required file'}, 201
        # user_id of calling api user
        user_id = request.form.get('user_id')
        id_album = request.form.get('id_album')
        description = request.form.get('description')
        # VALIDATE
        if (id_album == None):
            return {'message': 'id_album is required'}, HTTP_NotAccept['code']
        if user_id == None or user_id.isdigit() == False:
            return {'message': 'user_id (int) is required'}, HTTP_NotAccept['code']
        chech_user =  User.query.filter_by(id=user_id).first()
        if chech_user == None:
            return {'message': 'user_id not found : '+str(user_id) }, HTTP_NotFound['code']
        file_data = None
        try:
            file_data = request.files['file']
        except Exception as err:
            return {'message': str(err)}, HTTP_NotAccept['code']
        file_name = file_data.filename
        if file_name == None or file_name == "":
            return {'message': 'File name is invalid'}, HTTP_NotAccept['code']
        file_extension = get_extension(file_name)
        if file_extension not in allow_extension:
            return {'message': 'File extension is not allow'}, HTTP_NotAccept['code']
        chech_album = Album.query.filter_by(id=id_album).first()
        if (chech_album==None):
            return {'message': 'Not found album id :'+str(id_album)}, 404
        # END VALIDATE
        # CREATE DIR FOR ALBUM
        try:
            # PREPARE INFORMATION
            album_path = storage_path+"/"+str(id_album)
            create_dir(album_path)
            save_name= str(int(time.time()))+ "_"+ file_name
            storage_file_path = os.path.join(album_path, save_name)
            file_data.save(storage_file_path)
            date_upload = get_current_time()
            # CREATE PHOTO
            photo = Photo(
                id_album=id_album,
                name= file_name,
                save_name= save_name,
                path= storage_file_path,
                date_created=date_upload,
                description= description
                )
            # SAVE TO DB
            db.session.add(photo)
            db.session.commit()
            result = photo_schema.dump(photo)
            return {"status": 'success', 'data': result[0]}, 200
        except Exception as err:
            return {'message': str(err)}, HTTP_Forbidden['code']
