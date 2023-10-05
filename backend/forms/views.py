from rest_framework.views import APIView
from rest_framework.response import Response as resp
from rest_framework import status
from .serializers import *
from .utils import add_questions, get_form_data

from accounts.models import AccountsUser
from .models import *

class NewFormAPI(APIView):
    def post(self, request):
        user_id = request.session.get('user_id', 1)
        user = AccountsUser.objects.get(id=user_id)

        request_data = request.data
        try:
            form = Form.objects.create(
                title=request_data.get('title', None),
                creator=user
            )

            add_questions(form=form, request_data=request_data)

        except Exception as e:
            return resp(data=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return resp(data='Form created', status=status.HTTP_200_OK)
    
    def get(self, request):
        user_id = request.session.get('user_id', 1)
        user = AccountsUser.objects.get(id=user_id)
        
        form_id = request.query_params.get('form_id', None)
        
        try:
            if form_id:
                serialized_data: dict = get_form_data(form_id=form_id, user=user)
            else:
                forms_queryset = Form.objects.filter(creator=user)
                serialized_data = FormSerializer(forms_queryset, many=True).data
        except Exception as e:
            return resp(data=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return resp(data=serialized_data, status=status.HTTP_200_OK)
    

class AnswerFormAPI(APIView):

    def post(self, request):
        user_id = request.session.get('user_id', 1)
        user = AccountsUser.objects.get(id=user_id)

        request_data = request.data
        try:
            form = Form.objects.get(id=request_data.get('form_id'))
            response = Response.objects.create(
                form=form,
                user=user,
            )
            for question in request_data.get('questions', []):
                if question.get('answer'):
                    Answer.objects.create(
                        response=response,
                        question=Question.objects.get(id=question.get('question_id')),
                        text_answer=question.get('answer')
                    )
        except Exception as e:
            return resp(data=str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return resp(data='Answers added', status=status.HTTP_200_OK)