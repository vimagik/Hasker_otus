import factory
import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate
from django.contrib.auth import get_user_model

from questions.models import Questions, Answers, Tags
from api.views import GetQuestion, GetSearchQuestion, GetAnswers


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tags

    name = factory.Faker('name')


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class QuestionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Questions


class AnswersFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Answers

    correct = True


class IndexApiTest(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.view = GetQuestion.as_view({'get': 'list'})
        self.url = reverse('api:index')
        self.user = self.setup_user()
        user = UserFactory(username='Test_user')
        for i in range(25):
            QuestionFactory(title='Test_name', author=user)

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )

    def test_index_unauthorized(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_index_authorized(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response.render()
        response_dict = json.loads(response.content)
        self.assertGreater(len(response_dict['next']), 1)
        self.assertEqual(response_dict['count'], 25)


class GetQuestionApiTest(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.view = GetQuestion.as_view({'get': 'retrieve'})
        self.url = reverse('api:getquestion', args=(1,))
        self.user = self.setup_user()
        user = UserFactory(username='Test_user')
        question = QuestionFactory(title='Test_name', author=user)
        for i in range(3):
            tag = TagFactory()
            question.tags.add(tag)

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )

    def test_get_question_unauthorized(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_question_authorized(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response.render()
        response_dict = json.loads(response.content)
        self.assertEqual(response_dict['title'], 'Test_name')
        self.assertEqual(len(response_dict['tags']), 3)


class GetSearchRequestApiTest(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.view = GetSearchQuestion.as_view({'get': 'list'})
        self.url = reverse('api:searchresult') + '?search=Test'
        self.user = self.setup_user()
        user = UserFactory(username='Test_user')
        for i in range(25):
            QuestionFactory(title='Test_name', author=user)

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )

    def test_search_result_unauthorized(self):
        request = self.factory.get(self.url)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_question_authorized(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        response = self.view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response.render()
        response_dict = json.loads(response.content)
        self.assertGreater(len(response_dict['next']), 1)
        self.assertEqual(response_dict['count'], 25)


class GetAnswersApiTest(APITestCase):
    def setUp(self) -> None:
        self.factory = APIRequestFactory()
        self.view = GetAnswers.as_view({'get': 'list'})
        self.url = reverse('api:getanswers', args=(1,))
        self.user = self.setup_user()
        user = UserFactory(username='Test_user')
        question = QuestionFactory(title='Test_name', author=user)
        for i in range(25):
            AnswersFactory(question=question, author=user)

    @staticmethod
    def setup_user():
        User = get_user_model()
        return User.objects.create_user(
            'test',
            email='testuser@test.com',
            password='test'
        )

    def test_get_answer_unauthorized(self):
        request = self.factory.get(self.url)
        response = self.view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_get_answer_authorized(self):
        request = self.factory.get(self.url)
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response.render()
        response_dict = json.loads(response.content)
        self.assertGreater(len(response_dict['next']), 1)
        self.assertEqual(response_dict['count'], 25)
