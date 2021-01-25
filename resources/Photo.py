from flask import request
from flask_restful import Resource
from Model import *
import json
photos_schema = PhotoSchema(many=True)
photo_schema = PhotoSchema()
class PhotoResource(Resource):
    @staticmethod
    def get():
        photos = Photo.query.all()
        photos = photos_schema.dumps(photos)
        return {'status': 'success', 'data': photos}, 200
    @staticmethod
    def post():
        json_data = request.get_json(force=True)
        if not json_data:
               return {'message': 'No input data provided'}, 400
        # Validate and deserialize input
        response = json.dumps(json_data)
        data = photo_schema.loads(response)
        photo = Photo.query.filter_by(name=data['name']).first()
        if photo:
            return {'message': 'Photos already exists'}, 400
        photo = Photo(
            id_album=data['id_album'],
            name=data['name'],
            path=data['path'],
            date_created=data['date_created'],
            description=data['description']
            )
        db.session.add(photo)
        db.session.commit()
        result = photo_schema.dump(photo)
        return {"status": 'success', 'data': result}, 201