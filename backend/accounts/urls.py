from django.urls import path
from .views import *


urlpatterns = [
    path('signup/', RegisterApi.as_view(), name='sigup'),
    path('login/', LoginAPi.as_view(), name='login'),
    path('feedback/', FeedbackApi.as_view(), name='feedback'),

    path('get_info/', GetUser.as_view(), name='get_info'),
    path('my_feedbacks/', MyFeedbacks.as_view(), name='feedback'),
    path('top_rating/', TopRatedUsersView.as_view(), name='top_rating'),
]