from flask import jsonify

from auth.auth import AuthError


def setup_error_handling(app):
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
