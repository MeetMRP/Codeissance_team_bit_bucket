from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *
from .utils import get_subject
from django.core.mail import EmailMessage
from django.db.models import Avg, Count, F, Func

class RegisterApi(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data 

        return Response(user_data, status=status.HTTP_201_CREATED)


class LoginAPi(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user_data = serializer.data
        request.session['user_id'] = user_data.get('user_id')

        return Response(user_data, status=status.HTTP_200_OK)
    
class FeedbackApi(APIView):
    serializer_class = FeedbackSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data 

        return Response(user_data, status=status.HTTP_201_CREATED)
    
class SendMail(APIView):

    def post(self, request):
        user_id = request.session.get('user_id', 1)
        user = AccountsUser.objects.get(id=user_id)

        request_data = request.data
        email_subject = get_subject(event=request_data.get('event'), user_name=user.name)
        email_body = 'happy Birthday'
        email_receiver = request_data.email
        try:
            email = EmailMessage(
                    subject=email_subject, 
                    body=email_body, 
                    to=[email_receiver]
                    )
            email.send()
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

# home page api -> avg rating, user data, top 5 avg rating employee, all feedbakcs
class GetUser(APIView):

    def get(self, request):
        user_id = request.session.get('user_id', 1)
        user = AccountsUser.objects.get(id=user_id)

        try:
            serializer = UserSerializer(user).data
            serializer['profile_picture'] = serializer['profile_picture'][1:]
            feedbacks = Feedback.objects.filter(
                receiver=user    
            )
            print(feedbacks.count())
            count = feedbacks.count()
            feedback_serialiser = FeedbackSerializer(feedbacks, many=True).data
            rate = 0
            for feedback in feedback_serialiser:
                rate += feedback.get('rating')
            avg_rating = float(rate/ count)
            serializer['avg_rating'] = avg_rating

        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

        return Response(data=serializer, status=status.HTTP_200_OK)


class MyFeedbacks(APIView):

    def get(self, request):
        user_id = request.session.get('user_id', 1)
        user = AccountsUser.objects.get(id=user_id)

        try:
            feedbacks = Feedback.objects.filter(receiver=user).order_by('rating')
            serializer = FeedbackSerializer(feedbacks, many=True).data
        except Exception as e:
            return Response(str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

        return Response(data=serializer, status=status.HTTP_200_OK)    
    
class Round(Func):
    function = 'ROUND'
    template = '%(function)s(%(expressions)s, 2)'

class TopRatedUsersView(APIView):
    
    def get(self, request, *args, **kwargs):

        users_with_avg_rating = AccountsUser.objects.annotate(
            average_rating=Round(Avg('feedbacks_receiver__rating')),
            feedback_count=Count('feedbacks_receiver')
        ).filter(feedback_count__gt=0).order_by('-average_rating')[:5]

        serializer = UserRatingSerializer(users_with_avg_rating, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)