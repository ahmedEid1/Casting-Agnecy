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
        res = self.client().get('/actors')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data['actors']), 0)

    def test_get_actor(self):
        actors = Actor.query.all()
        actor_id = actors[0].id
        res = self.client().get('/actors/' + actor_id)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['actor'].id, actor_id)

    def test_actor_create(self):
        actor = {
            'name': "test_user",
            'age': 5,
            'gender': 'male'
        }
        res = self.client().post('/actors/add', data=json.dumps(actor), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['actor'].age, 5)

    def test_actor_edit(self):
        edit_data = {
            "age": 4
        }
        actors = Actor.query.all()
        actor_id = actors[-1].id
        res = self.client.patch('actors/edit/' + actor_id, data=json.dumps(edit_data), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['actor'].age, 4)
        self.assertEqual(data['actor'].name, "test_user")

    def test_actor_delete(self):
        actors = Actor.query.all()
        actor_id = actors[-1].id
        res = self.client().delete('/actors/' + actor_id)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['id'], actor_id)

    # actors endpoints success
    def test_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data['movies']), 0)

    def test_get_movie(self):
        movies = Movie.query.all()
        movie_id = movies[0].id
        res = self.client().get('/movies/' + movie_id)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['movie'].id, movie_id)

    def test_movie_create(self):
        movie = {
            'title': "test_movie",
            'release_date': datetime.now()
        }
        res = self.client().post('/movies/add', data=json.dumps(movie),
                                 headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['movie'].age, "test_movie")

    def test_movie_edit(self):
        edit_data = {
            "title": "new_title"
        }
        movies = Movie.query.all()
        movie_id = movies[-1].id
        time = movies[-1].id.release_date
        res = self.client.patch('actors/edit/' + movie_id, data=json.dumps(edit_data),
                                headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['movie'].title, "new_title")
        self.assertEqual(data['movie'].release_date, time)

    def test_movie_delete(self):
        movies = Movie.query.all()
        movie_id = movies[-1].id
        res = self.client().delete('/movies/' + movie_id)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['id'], movie_id)

    def test_wrong_method(self):
        res = self.client().post('/categories')
        self.assertEqual(res.status_code, 405)

    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data['questions']), 0)

    def test_zero_questions(self):
        res = self.client().get('/questions?page=100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_question_delete(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['id'], 5)

    def test_400_bad_delete(self):
        res = self.client().delete('/questions/1000')
        self.assertEqual(res.status_code, 400)

    def test_question_insert(self):
        info = {
            'question': "how are you",
            'answer': "fine",
            'category': 4,
            'difficulty': 1
        }
        res = self.client().post('/questions/add', data=json.dumps(info), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['question']), 5)

    def test_not_complete_question_insert(self):
        info = {
            'answer': "fine",
            'category': 4,
            'difficulty': 1
        }
        res = self.client().post('/questions/add', data=json.dumps(info), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], "Bad Request")

    def test_search_word(self):
        info = {
            'searchTerm': "1"
        }
        res = self.client().post('/questions', data=json.dumps(info), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data['questions']), 0)

    def test_searchTerm_not_str(self):
        info = {
            'searchTerm': 1
        }
        res = self.client().post('/questions', data=json.dumps(info), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)

    def test_get_questions_by_category(self):
        res = self.client().get("categories/5/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(data['questions']), 0)

    def test_404_category_not_found(self):
        res = self.client().get("categories/100/questions")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['message'], "Not Found")

    def test_get_quiz_question(self):
        info = {
            "quiz_category": {
                "id": 2,
            },
            "previous_questions": [1, 2, 3]
        }
        res = self.client().post("/quizzes", data=json.dumps(info), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(data['question']), 5)

    def test_wrong_category_id(self):
        info = {
            "quiz_category": {
            },
            "previous_questions": [1, 2, 3]
        }
        res = self.client().post("/quizzes", data=json.dumps(info), headers={'Content-Type': 'application/json'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['message'], "Bad Request")


if __name__ == "__main__":
    unittest.main()