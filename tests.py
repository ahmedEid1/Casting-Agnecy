import os
import unittest
import json
from datetime import datetime

from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import Actor, Movie, setup_db


class AgencyTestCase(unittest.TestCase):
    """This class represents the agency api test case"""

    def setUp(self):
        # load variables from .env file
        load_dotenv(dotenv_path="./.env")

        # load a token for every different role
        self.producer_token = "Bearer " + os.environ.get("producer_token")
        self.director_token = "Bearer " + os.environ.get("director_token")
        self.assistant_token = "Bearer " + os.environ.get("assistant_token")

        """Define test variables and initialize app."""
        self.database_path = os.environ.get("TEST_DATABASE_URL")
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        #  insert an actor and a movie into the db
        actor = {
            'name': "test_user",
            'age': 5,
            'gender': 'male'
        }
        self.client().post('/actors/add', data=json.dumps(actor), headers={'Content-Type': 'application/json',
                                                                           'Authorization': self.producer_token})

        movie = {
            'title': "test_movie",
            'release_date': str(datetime.now())
        }
        self.client().post('/movies/add', data=json.dumps(movie),
                           headers={'Content-Type': 'application/json', 'Authorization': self.producer_token})

    def tearDown(self):
        pass

    # actors endpoints success
    def test_get_actors(self):
        res = self.client().get('/actors', headers={'Authorization': self.producer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data['actors']), 0)

    def test_get_actor(self):
        actors = Actor.query.all()
        actor_id = actors[0].id
        res = self.client().get('/actors/' + str(actor_id), headers={'Authorization': self.producer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['actor']['id'], actor_id)

    def test_actor_create(self):
        actor = {
            'name': "test_user",
            'age': 5,
            'gender': 'male'
        }
        res = self.client().post('/actors/add', data=json.dumps(actor), headers={'Content-Type': 'application/json',
                                                                                 'Authorization': self.producer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        print(actor)
        self.assertEqual(data['actor']["age"], 5)

    def test_actor_edit(self):
        actor = {
            'name': "test_user",
            'age': 5,
            'gender': 'male'
        }
        res = self.client().post('/actors/add', data=json.dumps(actor),
                                 headers={'Content-Type': 'application/json', 'Authorization': self.producer_token})
        json.loads(res.data)
        edit_data = {
            "age": 4
        }
        actors = Actor.query.all()
        actor_id = actors[-1].id
        res = self.client().patch('actors/edit/' + str(actor_id), data=json.dumps(edit_data),
                                  headers={'Content-Type': 'application/json', 'Authorization': self.producer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['actor']['age'], 4)
        self.assertEqual(data['actor']['name'], "test_user")

    def test_actor_delete(self):
        actors = Actor.query.all()
        actor_id = actors[-1].id
        res = self.client().delete('/actors/' + str(actor_id), headers={'Authorization': self.producer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['id'], actor_id)

    # movies endpoints success
    def test_get_movies(self):
        res = self.client().get('/movies', headers={'Authorization': self.producer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data['movies']), 0)

    def test_get_movie(self):
        movies = Movie.query.all()
        movie_id = movies[0].id
        res = self.client().get('/movies/' + str(movie_id), headers={'Authorization': self.producer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['movie']['id'], movie_id)

    def test_movie_create(self):
        movie = {
            'title': "test_movie",
            'release_date': str(datetime.now())
        }
        res = self.client().post('/movies/add', data=json.dumps(movie),
                                 headers={'Content-Type': 'application/json', 'Authorization': self.producer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['movie']['title'], "test_movie")

    def test_movie_edit(self):
        edit_data = {
            "title": "new_title"
        }
        movies = Movie.query.all()
        movie_id = movies[-1].id
        time = movies[-1].release_date
        res = self.client().patch('movies/edit/' + str(movie_id), data=json.dumps(edit_data),
                                  headers={'Content-Type': 'application/json', 'Authorization': self.producer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['movie']['title'], "new_title")
        self.assertEqual(data['movie']['release_date'], str(time))

    def test_movie_delete(self):
        movies = Movie.query.all()
        movie_id = movies[-1].id
        res = self.client().delete('/movies/' + str(movie_id), headers={'Authorization': self.producer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['id'], movie_id)

    # actors error behaviour
    def test_wrong_get_actors(self):
        res = self.client().post('/actors', headers={'Authorization': self.producer_token})
        json.loads(res.data)
        self.assertEqual(res.status_code, 405)

    def test_wrong_get_actor(self):
        res = self.client().post('/actors/1000000000000', headers={'Authorization': self.producer_token})
        json.loads(res.data)
        self.assertEqual(res.status_code, 405)

    def test_wrong_delete_actor(self):
        res = self.client().delete('/actors/10000000000000', headers={'Authorization': self.producer_token})
        json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    def test_wrong_create_actor(self):
        actor = {
            'name': "test_user",
            'age': "not a number",
            'gender': 'male'
        }
        res = self.client().post('/actors/add', data=json.dumps(actor), headers={'Content-Type': 'application/json',
                                                                                 'Authorization': self.producer_token})
        json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    def test_wrong_edit_actor(self):
        edit_data = {
            "age": "not a number"
        }
        actors = Actor.query.all()
        actor_id = actors[-1].id
        res = self.client().patch('actors/edit/' + str(actor_id), data=json.dumps(edit_data),
                                  headers={'Content-Type': 'application/json', 'Authorization': self.producer_token})
        json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    # movies error behaviour
    def test_wrong_get_movies(self):
        res = self.client().post('/movies', headers={'Authorization': self.producer_token})
        json.loads(res.data)
        self.assertEqual(res.status_code, 405)

    def test_wrong_get_movie(self):
        res = self.client().post('/movies/100000000000000', headers={'Authorization': self.producer_token})
        json.loads(res.data)
        self.assertEqual(res.status_code, 405)

    def test_wrong_delete_movie(self):
        res = self.client().delete('/movies/100000000', headers={'Authorization': self.producer_token})
        json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    def test_wrong_create_movie(self):
        movie = {
            'title': "test_movie",
            'release_date': "not a date"
        }
        res = self.client().post('/movies/add', data=json.dumps(movie),
                                 headers={'Content-Type': 'application/json', 'Authorization': self.producer_token})
        json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    def test_wrong_edit_movie(self):
        movie = {
            'title': "test_movie",
            'release_date': str(datetime.now())
        }
        self.client().post('/movies/add', data=json.dumps(movie),
                           headers={'Content-Type': 'application/json', 'Authorization': self.producer_token})

        edit_data = {
            "release_date": "not a date"
        }
        movies = Movie.query.all()
        movie_id = movies[-1].id

        res = self.client().patch('movies/edit/' + str(movie_id), data=json.dumps(edit_data),
                                  headers={'Content-Type': 'application/json', 'Authorization': self.producer_token})
        json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    # testing RBAC permissions
    def test_assistant_right_permission(self):
        # can view actors
        res = self.client().get('/actors', headers={'Authorization': self.assistant_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data['actors']), 0)

        # can view movies
        res = self.client().get('/movies', headers={'Authorization': self.assistant_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data['movies']), 0)

    def test_assistant_wrong_permission(self):
        # can not create new actor
        actor = {
            'name': "not allowed",
            'age': 5,
            'gender': 'male'
        }
        res = self.client().post('/actors/add', data=json.dumps(actor), headers={'Content-Type': 'application/json','Authorization': self.assistant_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

        # can not create new movie
        movie = {
            'title': "not allowed",
            'release_date': str(datetime.now())
        }
        res = self.client().post('/movies/add', data=json.dumps(movie),
                                 headers={'Content-Type': 'application/json', 'Authorization': self.assistant_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_director_right_permission(self):
        # can add and delete an actor
        # add
        actor = {
            'name': "allowed",
            'age': 5,
            'gender': 'male'
        }
        res = self.client().post('/actors/add', data=json.dumps(actor),
                                 headers={'Content-Type': 'application/json', 'Authorization': self.director_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        # delete
        actors = Actor.query.all()
        actor_id = actors[-1].id
        res = self.client().delete('/actors/' + str(actor_id), headers={'Authorization': self.director_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        # can edit a movie
        edit_data = {
            "title": "new__title"
        }
        movies = Movie.query.all()
        movie_id = movies[-1].id
        time = movies[-1].release_date
        res = self.client().patch('movies/edit/' + str(movie_id), data=json.dumps(edit_data),
                                  headers={'Content-Type': 'application/json', 'Authorization': self.director_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_director_wrong_permission(self):
        # can not add or delete movies
        # add
        movie = {
            'title': "test__movie",
            'release_date': str(datetime.now())
        }
        res = self.client().post('/movies/add', data=json.dumps(movie),
                                 headers={'Content-Type': 'application/json', 'Authorization': self.director_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

        # delete
        movies = Movie.query.all()
        movie_id = movies[-1].id
        res = self.client().delete('/movies/' + str(movie_id), headers={'Authorization': self.director_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)

    def test_producer_actors_permission(self):
        # can do everything
        # can add and delete an actor
        # add
        actor = {
            'name': "allowed",
            'age': 5,
            'gender': 'male'
        }
        res = self.client().post('/actors/add', data=json.dumps(actor),
                                 headers={'Content-Type': 'application/json', 'Authorization': self.producer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        # delete
        actors = Actor.query.all()
        actor_id = actors[-1].id
        res = self.client().delete('/actors/' + str(actor_id), headers={'Authorization': self.producer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

    def test_producer_movies_permission(self):
        # can do everything
        # can add or delete movies
        # add
        movie = {
            'title': "test__movie",
            'release_date': str(datetime.now())
        }
        res = self.client().post('/movies/add', data=json.dumps(movie),
                                 headers={'Content-Type': 'application/json', 'Authorization': self.producer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)

        # delete
        movies = Movie.query.all()
        movie_id = movies[-1].id
        res = self.client().delete('/movies/' + str(movie_id), headers={'Authorization': self.producer_token})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)


if __name__ == "__main__":
    unittest.main()
