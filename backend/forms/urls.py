from django.urls import path
from .views import *


urlpatterns = [
    path('new_form/', NewFormAPI.as_view(), name='create_form'),
    path('answer_form/', AnswerFormAPI.as_view(), name='answer_form'),
]