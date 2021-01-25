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
        return {'status': 'success', 'data': albums}, 200

    @staticmethod
    def post():
        try:
            album_name = request.form.get('name')
            description = request.form.get('description')
            if album_name == None:
                return {'message': 'Album name is required'}, HTTP_NotAccept['code']
            album = Album.query.filter_by(name=album_name).first()
            if album:
                return {'message': 'Album name already exists'}, HTTP_NotAccept['code']
            date_created =  get_current_time()
            album = Album(
                name = album_name,
                description= description,
                date_created= date_created
            )
            db.session.add(album)
            db.session.commit()
            result = album_schema.dump(album)
            return {'status': 'success', 'data': result[0]}, 200
        except Exception as err:
            return {'message': str(err)}, HTTP_Forbidden['code']