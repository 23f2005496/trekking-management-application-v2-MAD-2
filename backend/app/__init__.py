from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from dotenv import load_dotenv

from app.cache import cache
from app.celery_app import make_celery
from flask_mail import Mail

mail = Mail()

migrate = Migrate()

login_manager = LoginManager()

db = SQLAlchemy()

def create_app():
    
    load_dotenv()
    
    app = Flask(__name__)
    app.config.from_object('config.settings.Config')
    app.config["JSON_SORT_KEYS"] = False


    app.config["CACHE_TYPE"] = "RedisCache"
    app.config["CACHE_REDIS_HOST"] = "localhost"
    app.config["CACHE_REDIS_PORT"] = 6379
    app.config["CACHE_DEFAULT_TIMEOUT"] = 300


    CORS(app, supports_credentials=True)
    
    db.init_app(app)
    migrate.init_app(app, db) 
    login_manager.init_app(app)
    cache.init_app(app)

    celery = make_celery(app)
    app.celery = celery

    mail.init_app(app)


    return app
