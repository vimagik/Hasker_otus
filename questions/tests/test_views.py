from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from questions.models import Questions, Answers, QuestionVotes, AnswerVotes


class IndexViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username='test_user',
        )
        for i in range(25):
            Questions.objects.create(
                title=f'title test {i}',
                body='test body',
                author=user,
            )

    def test_index_view_url_exist(self):
        resp = self.client.get('')
        self.assertEqual(resp.status_code, 200)

    def test_index_view_accessible_by_name(self):
        resp = self.client.get(reverse('questions:index'))
        self.assertEqual(resp.status_code, 200)

    def test_index_view_correct_template(self):
        resp = self.client.get(reverse('questions:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'questions/index.html')

    def test_index_view_pagination_is_twenty(self):
        resp = self.client.get(reverse('questions:index'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertEqual(resp.context['is_paginated'], True)
        self.assertEqual(len(resp.context['object_list']), 20)

    def test_index_view_all_questions(self):
        resp = self.client.get(reverse('questions:index')+'?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertEqual(resp.context['is_paginated'], True)
        self.assertEqual(len(resp.context['object_list']), 5)


class CreateQuestionViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='test_user',
            password='test',
        )

    def test_create_question_view_if_not_logged_in(self):
        resp = self.client.get(reverse('questions:createquestion'))
        self.assertRedirects(resp, '/auth/login/?next=/createquestion/')

    def test_index_view_url_exist(self):
        self.client.login(
            username='test_user',
            password='test',
        )
        resp = self.client.get('/createquestion/')
        self.assertEqual(resp.status_code, 200)

    def test_create_question_correct_template(self):
        self.client.login(
            username='test_user',
            password='test',
        )
        resp = self.client.get(reverse('questions:createquestion'))
        self.assertEqual(str(resp.context['user']), 'test_user')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed('questions/newQuestion.html')


class QuestionViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='test_user',
            password='test',
        )
        question = Questions.objects.create(
            title='test',
            body='test body',
            author=user,
        )
        for i in range(23):
            Answers.objects.create(
                body=f'test body {i}',
                author=user,
                correct=False,
                question=question,
            )

    def test_question_view_url_exist(self):
        resp = self.client.get('/question/1/')
        self.assertEqual(resp.status_code, 200)

    def test_question_view_object_doesnt_exist(self):
        resp = self.client.get('/question/2/')
        self.assertEqual(resp.status_code, 404)

    def test_question_view_accessible_by_name(self):
        resp = self.client.get(reverse('questions:questionview', args=(1,)))
        self.assertEqual(resp.status_code, 200)

    def test_question_view_correct_template(self):
        resp = self.client.get(reverse('questions:questionview', args=(1,)))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'questions/question_detail.html')

    def test_question_view_pagination_is_twenty(self):
        resp = self.client.get(reverse('questions:questionview', args=(1,)))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertEqual(resp.context['is_paginated'], True)
        self.assertEqual(len(resp.context['object_list']), 20)

    def test_question_view_all_questions(self):
        resp = self.client.get(reverse('questions:questionview', args=(1,))+'?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertEqual(resp.context['is_paginated'], True)
        self.assertEqual(len(resp.context['object_list']), 3)


class QuestionVoteViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='test_user',
            password='test',
        )
        Questions.objects.create(
            title='title test',
            body='test body',
            author=user,
        )

    def test_question_vote_if_not_logged_in(self):
        resp = self.client.get(reverse('questions:questionvote', args=(1,)))
        self.assertRedirects(resp, '/auth/login/?next=/question/1/vote/')

    def test_question_vote_url_exist(self):
        self.client.login(
            username='test_user',
            password='test',
        )
        resp = self.client.get('/question/1/vote/')
        self.assertEqual(resp.status_code, 302)

    def test_question_vote_true_redirect(self):
        self.client.login(
            username='test_user',
            password='test',
        )
        resp = self.client.get(reverse('questions:questionvote', kwargs={'pk': 1}) + '?page=1')
        self.assertRedirects(
            resp,
            reverse('questions:questionview', kwargs={'pk': 1}) + '?page=1',
            status_code=302
        )

    def test_question_vote_create(self):
        self.assertEqual(QuestionVotes.objects.all().count(), 0)
        self.client.login(
            username='test_user',
            password='test',
        )
        self.client.get(reverse('questions:questionvote', kwargs={'pk': 1}) + '?page=1')
        self.assertEqual(QuestionVotes.objects.all().count(), 1)


class QuestionUnVoteViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='test_user',
            password='test',
        )
        question = Questions.objects.create(
            title='title test',
            body='test body',
            author=user,
        )
        QuestionVotes.objects.create(
            author=user,
            question=question,
        )

    def test_question_unvote_if_not_logged_in(self):
        resp = self.client.get(reverse('questions:questionunvote', args=(1,)))
        self.assertRedirects(resp, '/auth/login/?next=/question/1/unvote/')

    def test_question_unvote_url_exist(self):
        self.client.login(
            username='test_user',
            password='test',
        )
        resp = self.client.get('/question/1/unvote/')
        self.assertEqual(resp.status_code, 302)


    def test_question_unvote_true_redirect(self):
        self.client.login(
            username='test_user',
            password='test',
        )
        resp = self.client.get(reverse('questions:questionunvote', kwargs={'pk': 1}) + '?page=1')
        self.assertRedirects(
            resp,
            reverse('questions:questionview', kwargs={'pk': 1}) + '?page=1',
            status_code=302
        )

    def test_question_unvote_delete_vote(self):
        self.assertEqual(QuestionVotes.objects.all().count(), 1)
        self.client.login(
            username='test_user',
            password='test',
        )
        self.client.get(reverse('questions:questionunvote', kwargs={'pk': 1}) + '?page=1')
        self.assertEqual(QuestionVotes.objects.all().count(), 0)


class AnswerVoteViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='test_user',
            password='test',
        )
        question = Questions.objects.create(
            title='title test',
            body='test body',
            author=user,
        )
        Answers.objects.create(
            body='test body',
            author=user,
            correct=False,
            question=question,
        )

    def test_answer_vote_if_not_logged_in(self):
        resp = self.client.get(reverse('questions:answervote', args=(1, 1, )))
        self.assertRedirects(resp, '/auth/login/?next=/question/1/1/vote/')

    def test_answer_vote_url_exist(self):
        self.client.login(
            username='test_user',
            password='test',
        )
        resp = self.client.get('/question/1/1/vote/')
        self.assertEqual(resp.status_code, 302)

    def test_answer_vote_true_redirect(self):
        self.client.login(
            username='test_user',
            password='test',
        )
        resp = self.client.get(reverse('questions:answervote', args=(1, 1,)) + '?page=1')
        self.assertRedirects(
            resp,
            reverse('questions:questionview', kwargs={'pk': 1}) + '?page=1',
            status_code=302
        )

    def test_answer_vote_create(self):
        self.assertEqual(AnswerVotes.objects.all().count(), 0)
        self.client.login(
            username='test_user',
            password='test',
        )
        self.client.get(reverse('questions:answervote', args=(1, 1,)) + '?page=1')
        self.assertEqual(AnswerVotes.objects.all().count(), 1)


class AnswerUnVoteViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='test_user',
            password='test',
        )
        question = Questions.objects.create(
            title='title test',
            body='test body',
            author=user,
        )
        answer = Answers.objects.create(
            body='test body',
            author=user,
            correct=False,
            question=question,
        )
        AnswerVotes.objects.create(
            author=user,
            answer=answer,
        )

    def test_answer_unvote_if_not_logged_in(self):
        resp = self.client.get(reverse('questions:answerunvote', args=(1, 1, )))
        self.assertRedirects(resp, '/auth/login/?next=/question/1/1/unvote/')

    def test_answer_unvote_url_exist(self):
        self.client.login(
            username='test_user',
            password='test',
        )
        resp = self.client.get('/question/1/1/unvote/')
        self.assertEqual(resp.status_code, 302)

    def test_answer_unvote_true_redirect(self):
        self.client.login(
            username='test_user',
            password='test',
        )
        resp = self.client.get(reverse('questions:answerunvote', args=(1, 1,)) + '?page=1')
        self.assertRedirects(
            resp,
            reverse('questions:questionview', kwargs={'pk': 1}) + '?page=1',
            status_code=302
        )

    def test_answer_unvote_delete(self):
        self.assertEqual(AnswerVotes.objects.all().count(), 1)
        self.client.login(
            username='test_user',
            password='test',
        )
        self.client.get(reverse('questions:answerunvote', args=(1, 1,)) + '?page=1')
        self.assertEqual(AnswerVotes.objects.all().count(), 0)


class AnswerSelectRightViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='test_user',
            password='test',
        )
        question = Questions.objects.create(
            title='title test',
            body='test body',
            author=user,
        )
        Answers.objects.create(
            body='test body',
            author=user,
            correct=False,
            question=question,
        )

    def test_answer_select_right_if_not_logged_in(self):
        resp = self.client.get(reverse('questions:setcorrectanswer', args=(1, 1, )))
        self.assertRedirects(resp, '/auth/login/?next=/question/1/1/setcorrectanswer/')

    def test_answer_select_right_url_exist(self):
        self.client.login(
            username='test_user',
            password='test',
        )
        resp = self.client.get('/question/1/1/setcorrectanswer/')
        self.assertEqual(resp.status_code, 302)

    def test_answer_select_correct_true_redirect(self):
        self.client.login(
            username='test_user',
            password='test',
        )
        resp = self.client.get(reverse('questions:setcorrectanswer', args=(1, 1,)) + '?page=1')
        self.assertRedirects(
            resp,
            reverse('questions:questionview', kwargs={'pk': 1}) + '?page=1',
            status_code=302
        )

    def test_answer_select_right_create(self):
        self.assertEqual(Answers.objects.get(id=1).correct, False)
        self.client.login(
            username='test_user',
            password='test',
        )
        self.client.get(reverse('questions:setcorrectanswer', args=(1, 1,)) + '?page=1')
        self.assertEqual(Answers.objects.get(id=1).correct, True)


class SearchQuestionViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username='test_user',
        )
        for i in range(22):
            Questions.objects.create(
                title=f'title test {i}',
                body='test body',
                author=user,
            )

    def test_search_question_view_url_exist(self):
        resp = self.client.get('/searchresult/?search=test')
        self.assertEqual(resp.status_code, 200)

    def test_search_question_view_accessible_by_name(self):
        resp = self.client.get(reverse('questions:searchresult') + '?search=test')
        self.assertEqual(resp.status_code, 200)

    def test_search_question_view_correct_template(self):
        resp = self.client.get(reverse('questions:searchresult') + '?search=test')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'questions/search_result.html')

    def test_search_question_pagination_is_twenty(self):
        resp = self.client.get(reverse('questions:searchresult') + '?search=test')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertEqual(resp.context['is_paginated'], True)
        self.assertEqual(len(resp.context['object_list']), 20)

    def test_search_question_all(self):
        resp = self.client.get(reverse('questions:searchresult')+'?search=test&page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertEqual(resp.context['is_paginated'], True)
        self.assertEqual(len(resp.context['object_list']), 2)

