from flask import Flask

def create_app():
    app = Flask(__name__)

    from .views import userskin, curation, recommend
    app.register_blueprint(userskin.bp)
    app.register_blueprint(curation.bp)
    app.register_blueprint(recommend.bp)

    return app