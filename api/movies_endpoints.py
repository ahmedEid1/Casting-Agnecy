from flask import request, jsonify, abort

from auth.auth import requires_auth


def setup_movies_endpoints(app, Movie):
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
