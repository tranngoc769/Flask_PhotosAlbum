from flask import Blueprint
from flask_restful import Api

from resources.Photo import *
from resources.Album import *
from resources.User import *

api_bp = Blueprint('api', __name__)
api = Api(api_bp)
template_bp = Blueprint('template', __name__)
template = Api(template_bp)

# # Route
# template.add_resource(IndexResource, '/')
# template.add_resource(AddUser, 'addUser')
# template.add_resource(AddDetails, 'addDetails')
api.add_resource(DeletePhotoResource,'/Photo/<string:photoid>/delete', endpoint='detelte photo')
api.add_resource(PhotoResource, '/Photo', endpoint='create photo')
# ALBUM
api.add_resource(AlbumsResource, '/Album')
# USER 
api.add_resource(UserResource, '/User')