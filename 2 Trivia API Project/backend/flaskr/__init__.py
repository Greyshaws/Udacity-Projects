import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

#pagination of questions
def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    setup_db(app)

    # Set up CORS. Allow '*' for origins
    CORS(app, resources={'/': {"origins": "*"}})
    
    # Use the after_request decorator to set Access-Control-Allow
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true')
        response.headers.add('Access-Control-Allow-Headers', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

   
    # An endpoint to handle GET requests for all categories
    @app.route('/categories')

    # get all categories and add to a dictionary
    def get_all_categories():
        categories_dict = {}
        for category in Category.query.all():
            categories_dict[category.id] = category.type
 
        # return 404 if no categories are found
        if len(categories_dict) == 0:
            abort(404)  

        # return a successful response
        return jsonify({
            'success': True,
            'categories': categories_dict
        })  

    # endpoint to handle GET requests for all questions
    @app.route('/questions')

    #get all questions and paginate
    def get_questions():
    questions = Question.query.all()
    total_questions = len(questions)
    current_questions = paginate_questions(request, questions)

    # get all categories and add to a dictionary
    def get_all_categories():
        categories_dict = {}
        for category in Category.query.all():
            categories_dict[category.id] = category.type

    # return 404 if no questions available
        if len(current_questions) == 0:
            abort(404)

    # return a successful response
        return jsonify({
           'success': True,
           'questions': current_questions,
           'total_questions': total_questions,
           'categories': categories_dict
        })

    # an endpoint to DELETE question using a question ID.
    @app.route('/questions/<int:id>', methods=['DELETE'])

    def delete_question(question_id):
        try:
            # get question by id
            question = Question.query.filter(Question.id == question_id).one_or_none()

            # return 404 if there are no questions
            if question is None:
                abort(404)

            # delete the question
            question.delete()

            # return a successful response
            return jsonify({
                'success': True,
                'deleted': question_id,
                'message': "Question deleted successfully!"
            })
        except:
            # return 422 if there is a problem deleting the question
            abort(422)

    # an endpoint to POST a new question,
    # which will require the question and answer text,
    # category, and difficulty score.
    @app.route('/questions', methods=['POST'])

    def post_question():

        # load the request body
        body = request.get_json()

        # get individual data from json body
        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)

        # validate to ensure all fields have data
        if ((new_question is None) or (new_answer is None)
             or (new_difficulty is None) or (new_category is None)):
           abort(422)

        try:
            # create new question
            question = Question(question=new_question, answer=new_answer,
                        difficulty=new_difficulty, category=new_category)
            
            # insert question
            question.insert()

            # return a successful response
            return jsonify({
                'success': True,
                'message': "Question created successfully!"
            })
        except:
            # return 422 status code if there's an error
            abort(422)
    
    # a POST endpoint to get questions based on a search term.
    # It should return any questions for whom the search term
    # is a substring of the question.
    @app.route('/questions/search', methods=['POST'])

    def search_questions():

        # get search term from request body
        body = request.get_json()
        search_term = body.get('searchTerm', None)

        # return 422 if an empty search erm is sent
        if search_term == None:
            abort(422)
        
        try:
            # query the database using the search term substring
            selection = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()

            # return 404 if no results are found
            if (len(selection) == 0):
                abort(404)

            # paginate the results
            paginated_selection = paginate_questions(request, selection)

            # return successful response
            return jsonify (
                {
                'success': True
                'questions': paginated_selection,
                'total_questions': len(Question.query.all())
                }
            )
        except:
            # return 404
            abort(404)

    # a GET endpoint to get questions based on category
    @app.route('/categories/<int:id>/questions')

    def get_question_by_category(category_id):

        # get category by id
        category = Category.query.filter(Category.id == category_id).one_or_none()

        # return 400 if category is not found
        if (category is None):
            abort(400)

        # get the questions
        questions = Question.query.filter_by(category=category_id).all()

        # paginate the selection
        paginated_selection = paginate_questions(request, questions)

        # return a succesful response
        return jsonify({
            'success': True,
            'questions': paginated_selection,
            'total_questions': len(Question.query.all()),
            'current_category': category.type
        })

    # a POST endpoint to get questions to play the quiz.
    # This endpoint should take category and previous question parameters
    # and return a random questions within the given category,
    # if provided, and that is not one of the previous questions.
    @app.route('/quizzes', methods=['POST'])

    def get_quiz_question():

        # load the request body
        body = request.get_json()

        # get previous questions
        previous_questions = body.get('previous_questions')

        # get category
        category = body.get('quiz_category')

        # return 400 if neither category or previous question is found
        if ((category is None) or (previous_questions is None)):
            abort(400)

        # load questions if default value of category is given
        if (category['id'] == 0):
            questions = Question.query.all()
        # else load questions filtered by category
        else: 
            questions = Question.query.filter_by(category=category['id']).all()

        # get random question
        def get_random_question():
            return questions[random.randrange(0, len(questions), 1)]

        # get random question for upcoming question
        upcoming_question = get_random_question

        # use boolean to check if question has been used before
        used = True 

        while used:
            if upcoming_question.id in previous_questions:
                upcoming_question = get_random_question()
            else:
                used = False

        # return a successful response
        return jsonify({
            'success': True,
            'question': upcoming_question.format(),
        })

    # error handlers
    # error handler for 404 (resource not found)
    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404
    
    # error handler for 400 (bad request)
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400
    
    # error handler for 422 (unprocessable entity)
    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable entity'
        }), 422
            







    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    return app

