from django.urls import path
from .views import *


urlpatterns = [
    path('signup/', RegisterApi.as_view(), name='sigup'),
    path('login/', LoginAPi.as_view(), name='login'),
    path('feedback/', FeedbackApi.as_view(), name='feedback'),
]