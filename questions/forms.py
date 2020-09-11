from django import forms
from questions.models import Questions, Answers


class QuestionCreateForm(forms.ModelForm):
    """Форма для добавления нового вопроса"""

    class Meta:
        model = Questions
        fields = ['title', 'body']

    tags = forms.CharField(max_length=50, label='Теги')

    def clean_tags(self):
        data = self.cleaned_data['tags']
        tags = data.split(',')
        if len(tags) > 3:
            raise forms.ValidationError('Укажите не более трех тегов')
        return data


class AnswerCreateForm(forms.ModelForm):
    """Форма для добавления ответа на вопрос"""
    class Meta:
        model = Answers
        fields = ['body']
