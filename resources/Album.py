from flask import request
from flask_restful import Resource
from Model import *
import json
from config import  *
from http_response import *
from util import  *
albums_schema = AlbumSchema(many=True)
album_schema = AlbumSchema()
class AlbumsResource(Resource):
    @staticmethod
    def get():
        albums = Album.query.all()
        albums = albums_schema.dump(albums)
        return {'status': 'success', 'data': json.loads(albums[0])}, 200
    @staticmethod
    def post():
        try:
            album_name = request.form.get('name')
            # user_id of calling api user
            user_id = request.form.get('user_id')
            description = request.form.get('description')
            if album_name == None:
                return {'message': 'Album name is required'}, HTTP_NotAccept['code']
            if user_id == None or user_id.isdigit() == False:
                return {'message': 'user_id (int) is required'}, HTTP_NotAccept['code']
            chech_user = User.query.filter_by(id=user_id).first()
            if chech_user == None:
                return {'message': 'user_id not found : '+str(user_id) }, HTTP_NotFound['code']
            if  chech_user.is_delete == 1:
                return {'message': 'user_id is deleted : '+str(user_id) }, HTTP_NotFound['code']
            album = Album.query.filter_by(name=album_name).first()
            if album:
                return {'message': 'Album name already exists'}, HTTP_NotAccept['code']
            date_created =  get_current_time()
            album = Album(
                name = album_name,
                description= description,
                date_created= date_created,
                user_id=user_id
            )
            db.session.add(album)
            db.session.commit()
            result = album_schema.dump(album)
            return {'status': 'success', 'data': result[0]}, 200
        except Exception as err:
            return {'message': str(err)}, HTTP_Forbidden['code']