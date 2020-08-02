from django.urls import path
from django.contrib.auth.decorators import login_required
from questions.views import *

app_name = 'questions'

urlpatterns = [
    path('', index, name='index'),
    path('createquestion/', login_required(CreateQuestionView.as_view()), name='createquestion'),
    path('question/<int:pk>/', QuestionView.as_view(), name='questionview')
]
