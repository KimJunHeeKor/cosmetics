from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    #environments
    app.config.from_envvar('APP_CONFIG_FILE')

    #ORM
    db.init_app(app)

    #Blueprint
    from .service import userskin, curation, recommend
    app.register_blueprint(userskin.bp)
    app.register_blueprint(curation.bp)
    app.register_blueprint(recommend.bp)

    return app