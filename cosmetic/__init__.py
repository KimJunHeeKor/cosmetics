from datetime import timedelta
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt


db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)

    #environments
    app.config.from_envvar('APP_CONFIG_FILE')
    # 토큰 생성에 사용될 Secret Key를 flask 환경 변수에 등록
    app.config["JWT_SECRET_KEY"] = "nCyC-COPERATION"
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)

    jwt.init_app(app) 
    bcrypt.init_app(app)
    
    #ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from cosmetic.model import db_models

    #Blueprint
    from .service import userskin, curation, recommend, login
    app.register_blueprint(userskin.bp)
    app.register_blueprint(curation.bp)
    app.register_blueprint(recommend.bp)
    app.register_blueprint(login.bp)

    return app