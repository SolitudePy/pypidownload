from flask import Flask

def create_app():
    app = Flask(__name__)

    from .main import routes

    app.register_blueprint(routes.main_bp)

    return app
