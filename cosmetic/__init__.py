from flask import Flask

def create_app():
    app = Flask(__name__)

    from .views import userskin, curation, recommand
    app.register_blueprint(userskin.bp)
    app.register_blueprint(curation.bp)
    app.register_blueprint(recommand.bp)

    return app