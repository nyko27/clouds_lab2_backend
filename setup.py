from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_cls: type):
    app = Flask(__name__)
    from flask_cors import CORS
    CORS(app)
    app.config.from_object(config_cls)

    db.init_app(app)

    with app.app_context():
        from controller import movie_routes, actor_routes, comment_routes, trailer_routes
        app.register_blueprint(movie_routes.movies)
        app.register_blueprint(actor_routes.actors)
        app.register_blueprint(trailer_routes.trailers)
        app.register_blueprint(comment_routes.comments)

    return app
