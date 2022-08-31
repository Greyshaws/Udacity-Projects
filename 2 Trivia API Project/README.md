# Trivia API Project
Trivia API is a webapp that allows people to test their knowledge through a trivia game. It uses a webpage to manage the trivia app and play the game.
The following functionality is implemented in the app:

   1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
  2. Delete questions.
  3. Add questions and require that they include question and answer text.
  4. Search for questions based on a text query string.
  5. Play the quiz game, randomizing either all questions or within a specific category.

## Getting Started

### Installing Dependencies

  1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

  2. **Virtual Environment** - It is recommended to work within a virtual environment for this project. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

  3. **PIP Dependencies** - After setting up your virtual environment, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM you will use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension you will use to handle cross-origin requests from the frontend server.

## Setting up the Database

With Postgres running, populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

## Run the server

Run the server from the `backend` directory. To do this, execute:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## Testing

To run tests, execute:

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

#### Frontend Dependencies

This project uses NPM to manage software dependecies. From the `frontend` directory, run:

```bash
npm install
```

## Running the Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use `npm start`. You can change the script in the `package.json` file.

Open http://localhost:3000 to view it in the browser. The page will reload if you make edits.

```bash
npm start
```

## API Reference

### Getting Started

- Backend Base URL: http://127.0.0.1:5000/

- Frontend Base URL: http://127.0.0.1:3000/

- Authentication: This project does not require authentication or API keys.

### Error Handling

Errors are returned as JSON in the following format:

```json
   {
    "success": "False",
    "error": 404,
    "message": "Resource not found"
   }
```
The API will return four types of error codes:

- 400 - bad request

- 404 - resource not found

- 422 - unprocessable entity

- 500 - internal server error

### Endpoints

`GET '/categories'`

- General:
 
    - Returns a list of all categories

- Sample: ```bash
             curl http://127.0.0.1:5000/categories
             ```

```json
       {
        "categories": {
            "1": "Science", 
            "2": "Art", 
            "3": "Geography", 
            "4": "History", 
            "5": "Entertainment", 
            "6": "Sports"
        }, 
        "success": true
    }
```

`GET '/questions'`

- General:

    - Returns a list of all questions

    - Questions are paginated in groups of 10

    - Also returns a list of categories and total number of questions.

- Sample: ```bash
             curl http://127.0.0.1:5000/questions
             ```

```json
      {
      "categories": {
          "1": "Science", 
          "2": "Art", 
          "3": "Geography", 
          "4": "History", 
          "5": "Entertainment", 
          "6": "Sports"
      }, 
      "questions": [
          {
              "answer": "Colorado, New Mexico, Arizona, Utah", 
              "category": 3, 
              "difficulty": 3, 
              "id": 164, 
              "question": "Which four states make up the 4 Corners region of the US?"
          }, 
          {
              "answer": "Muhammad Ali", 
              "category": 4, 
              "difficulty": 1, 
              "id": 9, 
              "question": "What boxer's original name is Cassius Clay?"
          }, 
          {
              "answer": "Apollo 13", 
              "category": 5, 
              "difficulty": 4, 
              "id": 2, 
              "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
          }, 
          {
              "answer": "Tom Cruise", 
              "category": 5, 
              "difficulty": 4, 
              "id": 4, 
              "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
          }, 
          {
              "answer": "Edward Scissorhands", 
              "category": 5, 
              "difficulty": 3, 
              "id": 6, 
              "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
          }, 
          {
              "answer": "Brazil", 
              "category": 6, 
              "difficulty": 3, 
              "id": 10, 
              "question": "Which is the only team to play in every soccer World Cup tournament?"
          }, 
          {
              "answer": "Uruguay", 
              "category": 6, 
              "difficulty": 4, 
              "id": 11, 
              "question": "Which country won the first ever soccer World Cup in 1930?"
          }, 
          {
              "answer": "George Washington Carver", 
              "category": 4, 
              "difficulty": 2, 
              "id": 12, 
              "question": "Who invented Peanut Butter?"
          }, 
          {
              "answer": "Lake Victoria", 
              "category": 3, 
              "difficulty": 2, 
              "id": 13, 
              "question": "What is the largest lake in Africa?"
          }, 
          {
              "answer": "The Palace of Versailles", 
              "category": 3, 
              "difficulty": 3, 
              "id": 14, 
              "question": "In which royal palace would you find the Hall of Mirrors?"
          }
      ], 
      "success": true, 
      "total_questions": 19
  }
```

`DELETE/questions/<int:id>`

- General:

    - Deletes a question by id using the url parameters.

    - Returns id of the deleted question when successful.

- Sample: ```bash
             curl http://127.0.0.1:5000/questions/6 -X DELETE
             ```

```json
      {
      "deleted": 6, 
      "success": true
  }
```

`POST/questions`

- General:

     - Creates a new question

- Sample: ```bash
             curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{ "question": "What is the capital of Nigeria?", "answer": "Abuja", "difficulty": 2, "category": "3" }'
             ```

```json
    {
      "success": true,
      "message": "Question created successfully!"
  }
```

`POST/questions/search`

- General:

     - Returns questions that have the search substring

- Sample: ```bash
             curl http://127.0.0.1:5000/questions/search -X POST -H "Content-Type: application/json" -d '{"searchTerm": "Peanut Butter"}'
             ```

```json
   {
  "questions": [
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    }
  ],
  "success": true,
  "total_questions": 20
}
```

`GET/categories/<int:id>/questions`

- General:
 
     - Gets questions by id using the url parameters.

     - Returns JSON object with matching questions that are paginated.

- Sample: ```bash
             curl http://127.0.0.1:5000/categories/1/questions
             ```

```json
  {
      "current_category": "Science", 
      "questions": [
          {
              "answer": "The Liver", 
              "category": 1, 
              "difficulty": 4, 
              "id": 20, 
              "question": "What is the heaviest organ in the human body?"
          }, 
          {
              "answer": "Alexander Fleming", 
              "category": 1, 
              "difficulty": 3, 
              "id": 21, 
              "question": "Who discovered penicillin?"
          }, 
          {
              "answer": "Blood", 
              "category": 1, 
              "difficulty": 4, 
              "id": 22, 
              "question": "Hematology is a branch of medicine involving the study of what?"
          }
      ], 
      "success": true, 
      "total_questions": 18
  }
```

`POST/quizzes`

- General:
 
    - Here, users play the quiz game.

    - Takes JSON request parameters of the category and previous questions

    - Returns JSON object with random question not in previous questions.

- Sample: ```bash
             curl http://127.0.0.1:5000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [4, 7], "quiz_category": {"type": "Science", "id": "1"}}'
             ```

```json
{
  "question": {
    "answer": "The Liver",
    "category": 1,
    "difficulty": 4,
    "id": 20,
    "question": "What is the heaviest organ in the human body?"
  },
  "success": true
}
```

## Authors

- Gracious Igwe worked on the API, test suite and this README to integrate with the frontend

- Udacity provided the starter files for this project including the models and frontend.