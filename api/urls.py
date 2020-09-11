from django.urls import path
from django.contrib.auth.decorators import login_required
from api.views import *

app_name = 'api'

urlpatterns = [
    path('getquestion/<int:pk>/', GetQuestion.as_view({'get': 'retrieve'}), name='getquestion'),
]
