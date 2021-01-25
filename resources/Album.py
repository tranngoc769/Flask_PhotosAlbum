from flask import request
from flask_restful import Resource
from Model import *
import json

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
        json_data = request.get_json(force=True)
        if not json_data:
            return {'message': 'No input data provided'}, 400
        # Validate data and deserialize inputs
        response = json.dumps(json_data)
        data = album_schema.loads(response)
        album = Album.query.filter_by(name=data['name']).first()
        if album:
            return {'message': 'Location already exists'}, 400
        album = Album(
            name = data['name'],
            description=data['description'],
            date_created=data['date_created']
        )
        db.session.add(album)
        db.session.commit()
        result = album_schema.dump(album)
        return {'status': 'success', 'data': result}, 201