import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from database.models import db_drop_and_create_all, setup_db, Drink
from auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)
db_drop_and_create_all()

# ROUTES

# a public endpoint to handle GET requests for all drinks
# contains only the drink.short() data representation
@app.route('/drinks')

def get_drinks():
    # query all drinks
    drinks = Drink.query.all()

    # return 404 if no drinks are found
    if len(drinks) == 0:
        abort(404)

    # format all drinks using .short()
    formatted_drinks = [drink.short() for drink in drinks]

    # return successful response
    return jsonify({
        'success': True,
        'drinks': formatted_drinks
    })


# an endpoint for to handle GET requests for detailed representation of drinks
# requires 'get:drinks-detail' permission
# contains drink.long() data representation
@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')

def get_drinks_detail(payload):
    # query all drinks
    drinks = Drink.query.all()

    # return 404 if no drinks are found
    #if len(drinks) == 0:
        #abort(404)

    # format using .long()
    formatted_drinks = [drink.long() for drink in drinks]

    # return successful response
    return jsonify({
        'success': True,
        'drinks': formatted_drinks
    }), 200


# an endpoint to POST new drinks
# creates a new row in the drinks table
# requires the 'post:drinks' permission
# contains the drink.long() data representation
@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')

def add_drink(payload):

    # load the request body
    body = request.get_json()

    # get data from json body
    title = body.get('title')
    recipe = body.get('recipe')

    # validate to ensure all fields have data
    if ((title is None) or (recipe is None)):
        abort(422)

    try:
        # create new drink
        drink = Drink(title=title, recipe=json.dumps(recipe))

        # insert drink
        drink.insert()

        # return a successful response
        return jsonify({
            'success': True,
            'drinks': drink.long()
        })
    except:
        # return 422 status code if there's an error
        abort(422)


# an endpoint to handle PATCH requests for editing existing drinks using a drink ID
# updates the corresponding row for <id>
# requires the 'patch:drinks' permission
# contains the drink.long() data representation
@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')

def patch_drink(payload, drink_id):

    # load the request body
    body = request.get_json()

    # get data from json body
    title = body.get('title', None)

    try:
        # get drink by id
        drink = Drink.query.filter_by(id=drink_id).one_or_none()

        # return 404 error if there's no drink
        if drink is None:
            abort(404)

        # return 400 if no title is given
        if title is None:
            abort(400)

        drink.title = title
        # update drink
        drink.update()

        # return successful response
        return jsonify({
            'success': True,
            'drinks': [drink.long()]
        })
    except:
        # return 422 status code if there's an error
        abort(422)


# an endpoint to DELETE drinks using a drink ID
# deletes the corresponding row for <id>
# requires the 'delete:drinks' permission
@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')

def delete_drink(payload, drink_id):
    try: 
        # get drink by id
        drink = Drink.query.filter_by(id=drink_id).one_or_none()

        # return 404 if no drink is found
        if drink is None:
            abort(404)

        # delete drink
        drink.delete()

        # return a successful response
        return jsonify({
            'success': True,
            'deleted': drink_id,
        }), 200
    except:
        # return 422 status code if there's an error
        abort(422)


# Error Handling
# error handler for 422 (unprocessable entity)
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

# error handler for 404 (resource not found)
@app.errorhandler(404)
def resource_not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

# error handler for 400 (bad request)
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400

@app.errorhandler(AuthError)
def authentication_error(error):
    status_code = error.status_code
    message = error.error#['description']

    return jsonify({
        'success': False,
        'error': status_code,
        'message': message
    }), status_code



#def handle_auth_error(exception):
    #response = jsonify(exception.error)
    #response.status_code = exception.status_code
    #return response
