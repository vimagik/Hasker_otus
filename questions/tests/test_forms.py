from django.test import TestCase

from questions.forms import QuestionCreateForm, AnswerCreateForm


class QuestionCreateFormTest(TestCase):

    def test_question_create_form_tags_label(self):
        form = QuestionCreateForm()
        self.assertEqual(form.fields['tags'].label, 'Теги')

    def test_question_create_form_valid(self):
        form_data = dict(
            tags='test,test2',
            title='test',
            body='test body'
        )
        form = QuestionCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_question_create_tags_count_error(self):
        form_data = dict(
            tags='test,test2,test3,test4',
            title='test',
            body='test body'
        )
        form = QuestionCreateForm(data=form_data)
        self.assertFalse(form.is_valid())


class AnswerCreateFormTest(TestCase):

    def test_answer_create_form_valid(self):
        form_data = {'body': 'test'}
        form = AnswerCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_answer_create_form_body_error(self):
        form_data = {'body': ''}
        form = AnswerCreateForm(data=form_data)
        self.assertFalse(form.is_valid())

