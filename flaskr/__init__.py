import os

from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate

from api.login_endpoint import setup_login
from error_handler import setup_error_handling
from models import setup_db, Movie, Actor, db
from api.actors_endpoints import setup_actors_endpoints
from api.movies_endpoints import setup_movies_endpoints


def create_app():
    load_dotenv(dotenv_path="./.env")

    # create and configure the app
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get("secret_key")
    setup_db(app)
    Migrate(app, db)
    '''
    CORS. Allow '*' for origins.
    '''
    CORS(app, resources={r"/*": {"origins": "*"}})

    '''
    after_request decorator sets Access-Control-Allow
    '''

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE")
        return response

    # the endpoints for the Actors and movies
    setup_actors_endpoints(app, Actor)
    setup_movies_endpoints(app, Movie)
    setup_login(app)
    # custom error handling
    setup_error_handling(app)

    return app


create_app()
