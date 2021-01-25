from flask import Flask
from flask_cors import CORS
from config import  *
from util import  *

def create_app(config_filename):
    app = Flask(__name__)
    CORS(app)
    app.config.from_object(config_filename)
    from app import api_bp, template_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    app.register_blueprint(template_bp, url_prefix='/')
    from Model import db
    db.init_app(app)
    create_dir(storage_path)
    return app
if __name__ == "__main__":
    app = create_app("config")
    app.run(host='127.0.0.1')