from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets

from api.serializers import QuestionSerializer
from questions.models import Questions


class GetQuestion(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Questions.objects.all()
