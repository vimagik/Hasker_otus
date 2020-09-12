from django.db.models import Count
from rest_framework.authentication import BasicAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from api.serializers import QuestionSerializer, TrendsSerializer, AnswerSerializer
from questions.models import Questions, Answers


class StandardResultsSetPagination(PageNumberPagination):
    """Pagination для index запроса"""
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100


class GetQuestion(viewsets.ModelViewSet):
    """Стандартная view для Question"""
    serializer_class = QuestionSerializer
    queryset = Questions.objects.all()
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated, )
    pagination_class = StandardResultsSetPagination

    def list(self, request, *args, **kwargs):
        response = super().list(request)
        trends = Questions.get_trends()
        trends_ser = TrendsSerializer(trends, many=True)
        response.data['trends'] = trends_ser.data
        return response


class GetSearchQuestion(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        search_string = self.request.GET.get('search')
        if search_string[:4] == 'tag:':
            queryset = Questions.objects.filter(tags__name__contains=search_string[4:]).annotate(
                count_votes=Count('questionvotes', distinct=True),
                count_answers=Count('answers', distinct=True)
            ).order_by('-count_votes', '-create_date')
        else:
            queryset = Questions.objects.filter(title__contains=search_string).annotate(
                count_votes=Count('questionvotes', distinct=True),
                count_answers=Count('answers', distinct=True)
            ).order_by('-count_votes', '-create_date')
        return queryset


class GetAnswers(viewsets.ModelViewSet):
    serializer_class = AnswerSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        return Answers.objects.filter(question_id=pk)

