from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config.from_envvar('APP_CONFIG_FILE')
    # app.config.from_object('config.py')

    #ORM
    db.init_app(app)

    from .views import userskin, curation, recommend
    app.register_blueprint(userskin.bp)
    app.register_blueprint(curation.bp)
    app.register_blueprint(recommend.bp)

    return app