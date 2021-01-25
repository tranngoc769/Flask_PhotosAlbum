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
    def __init__(self, name, date_created, description =""):
        self.name = name
        self.date_created = date_created
        self.description = description


class Photo(db.Model):
    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    save_name = db.Column(db.String(200), unique=True, nullable=False)
    id_album = db.Column(db.Integer, db.ForeignKey('album.id'), nullable=False)
    description = db.Column(db.String(1000), nullable=True)
    path = db.Column(db.String(1000), nullable=False)
    date_created = db.Column(db.DateTime, nullable= False)
    def __init__(self, name, id_album, description, path, date_created,save_name):
        self.name = name
        self.id_album = id_album
        self.description = description
        self.save_name = save_name
        self.path = path
        self.date_created = date_created


class AlbumSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    description = fields.String(required=False)
    date_created  = fields.DateTime(required=True)
class PhotoSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    id_album = fields.Integer(required=True)
    name = fields.String(required=True)
    save_name = fields.String(required=True)
    path = fields.String(required=True)
    description = fields.String(required=True)
    date_created = fields.DateTime(required=True)
