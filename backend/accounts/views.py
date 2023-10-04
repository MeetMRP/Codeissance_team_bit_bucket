from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import *


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