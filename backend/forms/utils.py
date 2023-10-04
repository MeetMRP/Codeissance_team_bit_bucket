from .models import *
from .serializers import *

def add_questions(form, request_data):
    for question_dict in request_data.get('questions', []):
        question = question_dict.get('question', '')
        question_type = question_dict.get('type', 'text')
        choices = question_dict.get('choices', [])

        question_obj = Question.objects.create(
            form=form,
            text=question,
            question_type=question_type
        )

        if question_type != 'text':
            for choice in choices:
                Choice.objects.create(
                    question=question_obj,
                    text=choice
                )

def get_choices(question) -> list:
    print(question.get('id'))
    question_obj = Question.objects.get(id=question.get('id'))
    choices = Choice.objects.filter(question=question_obj)
    choice_list = ChoiceSerializer(choices, many=True).data
    choice_response = []
    for choice in choice_list:
        choice_response.append(choice.get('text'))

    return choice_response

def add_answer(form_obj, user, question_obj):
    try:
        response = Response.objects.filter(
            form=form_obj,
            user=user
        ).last()

        answer = Answer.objects.get(
            response=response,
            question=question_obj
        )
    except:
        return ''
    return answer.text_answer

def get_form_data(form_id, user) -> dict:
    data = {}
    form = Form.objects.get(id=form_id)
    data['form_id'] = form_id
    data['title'] = form.title

    questions = Question.objects.filter(form=form)
    question_list = QuestionSerializer(questions, many=True).data
    questions_response = []

    for item in question_list:
        questions_data = {
                            "question_id": item["id"],
                            "question": item["text"],
                            "type": item["question_type"],
                        }
        if questions_data['type'] == 'multiple_choice':
            questions_data['choices'] = get_choices(question=item)
        questions_data['answer'] = add_answer(form_obj=form, user=user, question_obj=Question.objects.get(id=item["id"]))
        questions_response.append(questions_data)

    data['questions'] = questions_response
    return data