import os
import unittest
import json
from datetime import datetime

from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie


class AgencyTestCase(unittest.TestCase):
    """This class represents the agency api test case"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency"
        self.database_path = "postgresql://{}/{}".format('postgres:postgres@localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        pass

    # actors endpoints success
    def test_get_actors(self):
        actor = {
            'name': "test_user",
            'age': 5,
            'gender': 'male'
        }
        self.client().post('/actors/add', data=json.dumps(actor), headers={'Content-Type': 'application/json'})

        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data['actors']), 0)

    def test_get_actor(self):
        actors = Actor.query.all()
        actor_id = actors[0].id
        res = self.client().get('/actors/' + str(actor_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['actor']['id'], actor_id)

    def test_actor_create(self):
        actor = {
            'name': "test_user",
            'age': 5,
            'gender': 'male'
        }
        res = self.client().post('/actors/add', data=json.dumps(actor), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        print(actor)
        self.assertEqual(data['actor']["age"], 5)

    def test_actor_edit(self):
        edit_data = {
            "age": 4
        }
        actors = Actor.query.all()
        actor_id = actors[-1].id
        res = self.client().patch('actors/edit/' + str(actor_id), data=json.dumps(edit_data),
                                headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['actor']['age'], 4)
        self.assertEqual(data['actor']['name'], "test_user")

    def test_actor_delete(self):
        actors = Actor.query.all()
        actor_id = actors[-1].id
        res = self.client().delete('/actors/' + str(actor_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['id'], actor_id)

    # movies endpoints success
    def test_get_movies(self):
        movie = {
            'title': "test_movie",
            'release_date': str(datetime.now())
        }
        self.client().post('/movies/add', data=json.dumps(movie),
                           headers={'Content-Type': 'application/json'})
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data['movies']), 0)

    def test_get_movie(self):
        movies = Movie.query.all()
        movie_id = movies[0].id
        res = self.client().get('/movies/' + str(movie_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['movie']['id'], movie_id)

    def test_movie_create(self):
        movie = {
            'title': "test_movie",
            'release_date': str(datetime.now())
        }
        res = self.client().post('/movies/add', data=json.dumps(movie),
                                 headers={'Content-Type': 'application/json'})
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
                                headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['movie']['title'], "new_title")
        self.assertEqual(data['movie']['release_date'], str(time))

    def test_movie_delete(self):
        movies = Movie.query.all()
        movie_id = movies[-1].id
        res = self.client().delete('/movies/' + str(movie_id))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['id'], movie_id)

    # actors error behaviour
    def test_wrong_get_actors(self):
        res = self.client().post('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)

    def test_wrong_get_actor(self):
        res = self.client().post('/actors/1000000000000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)

    def test_wrong_delete_actor(self):
        res = self.client().delete('/actors/10000000000000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    def test_wrong_create_actor(self):
        actor = {
            'name': "test_user",
            'age': "not a number",
            'gender': 'male'
        }
        res = self.client().post('/actors/add', data=json.dumps(actor), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    def test_wrong_edit_actor(self):
        edit_data = {
            "age": "not a number"
        }
        actors = Actor.query.all()
        actor_id = actors[-1].id
        res = self.client().patch('actors/edit/' + str(actor_id), data=json.dumps(edit_data),
                                headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    # movies error behaviour
    def test_wrong_get_movies(self):
        res = self.client().post('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)

    def test_wrong_get_movie(self):
        res = self.client().post('/movies/100000000000000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)

    def test_wrong_delete_movie(self):
        res = self.client().delete('/movies/100000000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    def test_wrong_create_movie(self):
        movie = {
            'title': "test_movie",
            'release_date': "not a date"
        }
        res = self.client().post('/movies/add', data=json.dumps(movie),
                                 headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)

    def test_wrong_edit_movie(self):
        movie = {
            'title': "test_movie",
            'release_date': str(datetime.now())
        }
        self.client().post('/movies/add', data=json.dumps(movie),
                           headers={'Content-Type': 'application/json'})

        edit_data = {
            "release_date": "not a date"
        }
        movies = Movie.query.all()
        movie_id = movies[-1].id
        time = movies[-1].release_date
        res = self.client().patch('movies/edit/' + str(movie_id), data=json.dumps(edit_data),
                                headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)


if __name__ == "__main__":
    unittest.main()
