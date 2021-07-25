# import os
#
# from flask import Flask, request, abort, jsonify
# from flask_cors import CORS
# from flask_sqlalchemy import SQLAlchemy
#
# from auth.auth import AuthError, requires_auth
#
# from models import Actor, Movie
#
# # create and configure the app
# app = Flask(__name__)
# app.config['SECRET_KEY'] = os.environ["SECRET_KEY"]
#
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ['DATABASE_URL']
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#
# cors = CORS(app, resources={r"/*": {"origins": "*"}})
#
#
# @app.after_request
# def after_request(response):
#     response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
#     response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE")
#     return response
