import os

from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from auth.auth import AuthError, requires_auth

from models import setup_db, Actor, Movie

# create and configure the app
app = Flask(__name__)
app.config['SECRET_KEY'] = "dskdm"
setup_db(app)

cors = CORS(app, resources={r"/*": {"origins": "*"}})


@app.after_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE")
    return response


@app.route('/login-url')
def login():
    return jsonify(
        {
            "login-url": os.environ.get('login_url')
        }
    )


# get all the actors
@app.route('/actors', methods=['GET'])
@requires_auth("get:actors")
def get_actors(payload):
    try:
        response = {
            "actors": [actor.format() for actor in Actor.query.all()]
        }
        return jsonify(response)
    except:
        abort(500)


# get actors by id
@app.route('/actors/<int:actor_id>', methods=["GET"])
@requires_auth("get:actors")
def get_actor(payload, actor_id):
    try:
        actor = Actor.query.get(actor_id)
        return jsonify({"actor": actor.format()})
    except:
        abort(400)


# delete an actor
@app.route('/actors/<int:actor_id>', methods=["DELETE"])
@requires_auth("delete:actors")
def delete_actor(payload, actor_id):
    try:
        actor = Actor.query.get(actor_id)
        actor.delete()
        return jsonify({"id": actor_id})
    except:
        abort(400)


# add a new actor
@app.route("/actors/add", methods=['POST'])
@requires_auth("add:actors")
def create_actor(payload):
    try:
        actor = Actor(
            name=request.json['name'],
            age=request.json['age'],
            gender=request.json['gender']
        )

        actor.insert()

        actors = Actor.query.all()
        return jsonify(
            {
                "actor": actors[-1].format(),
            }
        )
    except:
        abort(400)


# edit an actor
@app.route("/actors/edit/<int:actor_id>", methods=['PATCH'])
@requires_auth("edit:actors")
def edit_actor(payload, actor_id):
    try:
        actor = Actor.query.get(actor_id)
        actor.name = request.json.get("name", actor.name)
        actor.age = int(request.json.get("age", actor.age))
        actor.gender = request.json.get("gender", actor.gender)
        actor.update()

        return jsonify({"actor": actor.format()})
    except:
        abort(400)


# get all movies
@app.route('/movies', methods=['GET'])
@requires_auth("get:movies")
def get_movies(payload):
    movies = [movie.format() for movie in Movie.query.order_by().all()]

    response = {
        "movies": movies,
    }
    return jsonify(response)


# get movies by id
@app.route('/movies/<int:movie_id>', methods=["GET"])
@requires_auth("get:movies")
def get_movie(payload, movie_id):
    try:
        movie = Movie.query.get(movie_id)
        return jsonify({"movie": movie.format()})
    except:
        abort(400)


# delete an actor
@app.route('/movies/<int:movie_id>', methods=["DELETE"])
@requires_auth("delete:movies")
def delete_movie(payload, movie_id):
    try:
        movie = Movie.query.get(movie_id)
        movie.delete()
        return jsonify({"id": movie_id})
    except:
        abort(400)


# add a movie
@app.route("/movies/add", methods=['POST'])
@requires_auth("add:movies")
def create_movie(payload):
    try:
        movie = Movie(
            title=request.json['title'],
            release_date=request.json['release_date']
        )

        movie.insert()

        movies = Movie.query.order_by(Movie.id).all()
        return jsonify(
            {
                "movie": movies[-1].format(),
            }
        )
    except:
        abort(400)


# add a movie
@app.route("/movies/edit/<int:movie_id>", methods=['PATCH'])
@requires_auth("edit:movies")
def edit_movie(payload, movie_id):
    try:
        movie = Movie.query.get(movie_id)
        movie.title = request.json.get("title", movie.title)
        movie.release_date = request.json.get("release_date", movie.release_date)
        movie.update()

        return jsonify({"movie": movie.format()})
    except:
        abort(400)


# error handling
@app.errorhandler(404)
def not_found(error):
    return jsonify(
        {
            "success": False,
            "error": 404,
            "message": "Not Found"
        }
    ), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify(
        {
            "success": False,
            "error": 405,
            "message": "method_not_allowed"
        }
    ), 405


@app.errorhandler(422)
def not_found(error):
    return jsonify(
        {
            "success": False,
            "error": 422,
            "message": "Unprocessable"
        }
    ), 422


@app.errorhandler(400)
def not_found(error):
    return jsonify(
        {
            "success": False,
            "error": 400,
            "message": "Bad Request"
        }
    ), 400


@app.errorhandler(500)
def not_found(error):
    return jsonify(
        {
            "success": False,
            "error": 500,
            "message": "server error"
        }
    ), 500


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.error['code'],
        "message": error.error['description']
    }), error.status_code
