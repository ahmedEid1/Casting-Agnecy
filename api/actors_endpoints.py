from flask import jsonify, abort, request

from auth.auth import requires_auth


# add the actors endpoints to the flask app
def setup_actors_endpoints(app, actor_model):

    # get all the actors
    @app.route('/actors', methods=['GET'])
    @requires_auth("get:actors")
    def get_actors():
        try:
            response = {
                "actors": [actor.format() for actor in actor_model.query.all()]
            }
            return jsonify(response)
        except:
            abort(500)

    # get actors by id
    @app.route('/actors/<int:actor_id>', methods=["GET"])
    @requires_auth("get:actors")
    def get_actor(actor_id):
        try:
            actor = actor_model.query.get(actor_id)
            return jsonify({"actor": actor.format()})
        except:
            abort(400)

    # delete an actor
    @app.route('/actors/<int:actor_id>', methods=["DELETE"])
    @requires_auth("delete:actors")
    def delete_actor(actor_id):
        try:
            actor = actor_model.query.get(actor_id)
            actor.delete()
            return jsonify({"id": actor_id})
        except:
            abort(400)

    # add a new actor
    @app.route("/actors/add", methods=['POST'])
    @requires_auth("add:actors")
    def create_actor():
        try:
            actor = actor_model(
                name=request.json['name'],
                age=request.json['age'],
                gender=request.json['gender']
            )

            actor.insert()

            actors = actor_model.query.all()
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
    def edit_actor(actor_id):
        try:
            actor = actor_model.query.get(actor_id)
            actor.name = request.json.get("name", actor.name)
            actor.age = int(request.json.get("age", actor.age))
            actor.gender = request.json.get("gender", actor.gender)
            actor.update()

            return jsonify({"actor": actor.format()})
        except:
            abort(400)
