from django.urls import path
from api.views import *

app_name = 'api'

urlpatterns = [
    path('getquestion/<int:pk>/', GetQuestion.as_view({'get': 'retrieve'}), name='getquestion'),
    path('index/', GetQuestion.as_view({'get': 'list'}), name='index'),
    path('searchresult/', GetSearchQuestion.as_view({'get': 'list'}), name='searchresult'),
    path('getanswers/<int:pk>/', GetAnswers.as_view({'get': 'list'}), name='getanswers'),
]
