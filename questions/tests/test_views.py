import base64

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from questions.models import Questions, Answers, QuestionVotes, AnswerVotes
from registration.models import UserProfile


class IndexViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username='test_user',
        )
        photo = SimpleUploadedFile(
            content=(base64.b64decode(TEST_IMAGE)),
            name='tempfile.png',
            content_type='image/png',
        )
        UserProfile.objects.create(
            user=user,
            photo=photo
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
        user = User.objects.create_user(
            username='test_user',
            password='test',
        )
        photo = SimpleUploadedFile(
            content=(base64.b64decode(TEST_IMAGE)),
            name='tempfile.png',
            content_type='image/png',
        )
        UserProfile.objects.create(
            user=user,
            photo=photo
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
        self.assertTemplateUsed('questions/new_question.html')


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
        for i in range(33):
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

    def test_question_view_pagination_is_thirty(self):
        resp = self.client.get(reverse('questions:questionview', args=(1,)))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertEqual(resp.context['is_paginated'], True)
        self.assertEqual(len(resp.context['object_list']), 30)

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
        photo = SimpleUploadedFile(
            content=(base64.b64decode(TEST_IMAGE)),
            name='tempfile.png',
            content_type='image/png',
        )
        UserProfile.objects.create(
            user=user,
            photo=photo
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
        photo = SimpleUploadedFile(
            content=(base64.b64decode(TEST_IMAGE)),
            name='tempfile.png',
            content_type='image/png',
        )
        UserProfile.objects.create(
            user=user,
            photo=photo
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
        photo = SimpleUploadedFile(
            content=(base64.b64decode(TEST_IMAGE)),
            name='tempfile.png',
            content_type='image/png',
        )
        UserProfile.objects.create(
            user=user,
            photo=photo
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
        photo = SimpleUploadedFile(
            content=(base64.b64decode(TEST_IMAGE)),
            name='tempfile.png',
            content_type='image/png',
        )
        UserProfile.objects.create(
            user=user,
            photo=photo
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
        photo = SimpleUploadedFile(
            content=(base64.b64decode(TEST_IMAGE)),
            name='tempfile.png',
            content_type='image/png',
        )
        UserProfile.objects.create(
            user=user,
            photo=photo
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

TEST_IMAGE = '''
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
'''.strip()

