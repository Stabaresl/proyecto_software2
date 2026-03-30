from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from app.utils.db import init_db
import os

load_dotenv()

def create_app():
    app = Flask(__name__)

    app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/tb_formacion')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'secret')

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    init_db(app)

    from app.routes.formacion_routes import formacion_bp
    from app.routes.acuerdo_routes import acuerdo_bp

    app.register_blueprint(formacion_bp, url_prefix='/api/formaciones')
    app.register_blueprint(acuerdo_bp,   url_prefix='/api/acuerdos')

    return app