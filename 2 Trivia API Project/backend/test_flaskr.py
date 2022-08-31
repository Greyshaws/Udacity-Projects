import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category
from utils import create_sample_question


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('postgres', 'taffetaz','localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # test for successful question pagination
    def test_get_paginated_questions(self):
        #get response
        response = self.client().get('/questions')
        # load data
        data = json.loads(response.data)
        # check status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        # check to see if total_questions and questions return data
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    # test for question pagination failure
    def test_404_sent_requesting_beyond_valid_page(self):
        # send request with error
        response = self.client().get('/questions?page=100')
        # load response
        data = json.loads(response.data)
        # check status code and message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # test to get all categories    
    def test_get_all_categories(self):
        # get response
        response = self.client().get('/categories')
        # load data
        data = json.loads(response.data)
        # check status code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['categories'])
        self.assertEqual(len(data['categories']), 6)

    # test for successful question deletion
    def test_delete_question(self):
        # gets id of sample question
        sample_question_id = create_sample_question()
        # deletes question sample and gets response
        response = self.client().delete('./questions/{}'.format(sample_question_id))
        # load data
        data = json.loads(response.data) 
        # check if question was deleted
        question = Question.query.filter(Question.id == 1).one_or_none()
        # check status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], "Question deleted successfully!")
        # check if question is None after deleting
        self.assertIsNone(question)

    # test for unsuccessful question deletion
    def test_422_unsuccessful_delete_question(self):
        # gets id of sample question
        sample_question_id = create_sample_question()
        # tests if question has already been deleted and gets response
        response = self.client().delete('/questions/{}'.format(sample_question_id))
        # load data
        data = json.loads(response.data)
        # check status code and message
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    # test for deleting question with invalid id
    def test_404_delete_question_with_invalid_id(self):
        # tests for invalid id
        response = self.client().delete('/questions/gthuohred32145f')
        # load data
        data = json.loads(response.data)
        # check status code and message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # test for successful creation of new question
    def test_create_question(self):
        # sample question
        sample_question = {
            'question': 'This is a sample question',
            'answer': 'this is a sample answer',
            'difficulty': 4,
            'category': 1,
        }
        # creates question 
        response = self.client().post('/questions', json=sample_question)
        # load data
        data = json.loads(response.data)
        # see if the question has been created
        question = Question.query.filter_by(question_id=data['created']).one_or_none()
        # check status code and success message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'Question created successfully')
        # check if question is not None
        self.assertIsNotNone(question)

    # test for unsuccessful creation
    def test_422_unsuccessful_create_question(self):
        request_data = {}
        # creates new questions with empty json data
        response = self.client().post('/questions', json=request_data)
        # load response
        data = json.loads(response.data)
        # check status code and message
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    # test for searching questions
    def test_search_questions(self):
        request_data = {
            'searchTerm': 'Peanut Butter',
        }
        # send request with request data
        response = self.client().post('/questions/search', json=request_data)
        # load data
        data = json.loads(response.data)
        # check status code
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        # check whether number of result is = 1
        self.assertEqual(len(data['questions']), 1)

    # test for empty search term
    def test_422_empty_search_term(self):
        response = self.client().post('/questions/search', json={'searchTerm': ''})
        # load data
        data = json.loads(response.data)
        # check status code and message
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable entity')

    # test for invalid search term
    def test_404_invalid_search_term(self):
        request_data = {
            'searchTerm': 'frhfjg548djhv74'
        }
        # send request with request data
        response = self.client().post('/questions/search', json=request_data)
        # load data
        data = json.loads(response.data)
        # check status code and message
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource not found')

    # test for getting questions by category
    def test_get_questions_by_category(self):
        # send request with category id 2 for Art
        response = self.client().get('/categories/2/questions')
        # load response data
        data = json.loads(response.data)
        # check status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        # check that questions are returned
        self.assertNotEqual(len(data['questions']), 0)
        # check that current category returned is Art
        self.assertEqual(data['current_category'], 'Art')

    # test for invalid category id
    def test_400_invalid_category_id(self):
         # send request with invalid id 585
        response = self.client().get('/categories/585/questions')
        # load response data
        data = json.loads(response.data)
        # check response status code and message
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # test for playing quiz game
    def test_play_quiz_game(self):
        request_data = {
            'previous_questions': [4, 7],
            'quiz_category': {
                'type': 'Sports',
                'id': 6
            }
        }
        # send request and process response
        response = self.client().post('/quizzes', json=request_data)
        # load response data
        data = json.loads(response.data)
        # check status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        # check that previous questions are not returned
        self.assertNotEqual(data['question']['id'], 4)
        self.assertNotEqual(data['question']['id'], 7)
        # check that returned question is in expected category
        self.assertEqual(data['question']['category'], 6)

    # test for unsuccessful quiz game
    def test_400_unsuccessful_quiz_game(self):
        request_data = {}
        # process response with empty json data
        response = self.client().post('/quizzes', json=request_data)
        # load data
        data = json.loads(response.data)
        # check status code and message
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad request error')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()