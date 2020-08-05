from django.urls import path
from django.contrib.auth.decorators import login_required
from questions.views import *

app_name = 'questions'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('createquestion/', login_required(CreateQuestionView.as_view()), name='createquestion'),
    path('question/<int:pk>/', QuestionView.as_view(), name='questionview'),
    path('question/<int:pk>/vote/', login_required(QuestionVoteView.as_view()), name='questionvote'),
    path('question/<int:pk>/unvote/', login_required(QuestionUnVoteView.as_view()), name='questionunvote'),
    path('question/<int:pk>/<int:id_answer>/vote/', login_required(AnswerVoteView.as_view()), name='answervote'),
    path('question/<int:pk>/<int:id_answer>/unvote/', login_required(AnswerUnVoteView.as_view()), name='answerunvote'),
    path('question/<int:pk>/<int:id_answer>/setcorrectanswer/',
         login_required(AnswerSelectRightView.as_view()), name='setcorrectanswer'),
]
