from models import Question

def create_sample_question():
    question = Question(
        question = 'This is a question sample',
        answer = 'This is a sample answer',
        difficulty = 1,
        category = '1'
    )

    question.insert()

    return question.id