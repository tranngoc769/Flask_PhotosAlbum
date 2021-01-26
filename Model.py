from flask import Flask
from marshmallow import Schema, fields, pre_load, validate, ValidationError
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


ma = Marshmallow()
db = SQLAlchemy()


class Album(db.Model):
    __tablename__ = 'album'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    name = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    date_created = db.Column(db.DateTime, nullable= False)
    user_id = db.Column(db.Integer, nullable=True)
    def __init__(self, name, date_created, user_id,description =""):
        self.name = name
        self.date_created = date_created
        self.description = description
        self.user_id = user_id

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    fullname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(1000), nullable=False)
    email = db.Column(db.String(100), nullable=True)
    date_created = db.Column(db.DateTime, nullable= False)
    role = db.Column(db.Integer,nullable=False, default=2)
    def __init__(self, username, fullname, password,email,date_created, role):
        self.username = username
        self.fullname = fullname
        self.password = password
        self.email = email
        self.date_created = date_created
        self.role = role
class Photo(db.Model):
    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    save_name = db.Column(db.String(200), unique=True, nullable=False)
    id_album = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    path = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, nullable= False)
    user_id = db.Column(db.Integer, nullable=True)
    def __init__(self, name, id_album, description, path, date_created,save_name, user_id):
        self.name = name
        self.id_album = id_album
        self.description = description
        self.save_name = save_name
        self.path = path
        self.date_created = date_created
        self.user_id = user_id
class AlbumSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(required=False)
    date_created  = fields.DateTime(required=True)
    user_id = fields.Integer(required=True)
class PhotoSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    id_album = fields.Integer(required=True)
    name = fields.String(required=True)
    save_name = fields.String(required=True)
    path = fields.String(required=True)
    description = fields.String(required=True)
    date_created = fields.DateTime(required=True)
    user_id = fields.Integer(required=True)
class UserSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    username = fields.Integer(required=True)
    fullname = fields.String(required=True)
    password = fields.String(required=True)
    email = fields.Email(required=True)
    date_created = fields.DateTime(required=True)
    role = fields.Integer(required=True)