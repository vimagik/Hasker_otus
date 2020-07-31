from django.urls import path
from django.contrib.auth.decorators import login_required
from questions.views import *

app_name = 'questions'

urlpatterns = [
    path('', index, name='index'),
    path('createquestion/', login_required(NewQuestionView.as_view()), name='createquestion')
]
