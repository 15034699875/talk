from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_socketio import SocketIO
import os
from .db_config import get_db_config

# 确保模型被导入
from .models import post

db = SQLAlchemy()
socketio = SocketIO(cors_allowed_origins="*")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev_secret')
    db_config = get_db_config()
    if db_config:
        app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        CORS(app)
        db.init_app(app)
        socketio.init_app(app)
        from .api import register_blueprints
        register_blueprints(app)
    else:
        from .api.db_setup import bp as db_setup_bp
        app.register_blueprint(db_setup_bp)
    return app 