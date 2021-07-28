import os

from flask import request, jsonify
from werkzeug.utils import redirect


def setup_login(app):

    @app.route('/callback')
    def callback_handling():
        return jsonify(
            {
                "access_token": "copy the access token from the url ^_^"
            }
        )

    @app.route('/login')
    def login():
        return redirect(os.environ.get("login_url"))


