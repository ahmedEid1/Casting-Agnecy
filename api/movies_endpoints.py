from flask import request, jsonify, abort

from auth.auth import requires_auth


def setup_movies_endpoints(app, movie_model):
    # get all movies
    @app.route('/movies', methods=['GET'])
    @requires_auth("get:movies")
    def get_movies():
        movies = [movie.format() for movie in movie_model.query.order_by().all()]

        response = {
            "movies": movies,
        }
        return jsonify(response)

    # get movies by id
    @app.route('/movies/<int:movie_id>', methods=["GET"])
    @requires_auth("get:movies")
    def get_movie(movie_id):
        try:
            movie = movie_model.query.get(movie_id)
            return jsonify({"movie": movie.format()})
        except:
            abort(400)

    # delete an actor
    @app.route('/movies/<int:movie_id>', methods=["DELETE"])
    @requires_auth("delete:movies")
    def delete_movie(movie_id):
        try:
            movie = movie_model.query.get(movie_id)
            movie.delete()
            return jsonify({"id": movie_id})
        except:
            abort(400)

    # add a movie
    @app.route("/movies/add", methods=['POST'])
    @requires_auth("add:movies")
    def create_movie():
        try:
            movie = movie_model(
                title=request.json['title'],
                release_date=request.json['release_date']
            )

            movie.insert()

            movies = movie_model.query.order_by(movie_model.id).all()
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
    def edit_movie(movie_id):
        try:
            movie = movie_model.query.get(movie_id)
            movie.title = request.json.get("title", movie.title)
            movie.release_date = request.json.get("release_date", movie.release_date)
            movie.update()

            return jsonify({"movie": movie.format()})
        except:
            abort(400)
