from django.db import models
from django.contrib.auth.models import User
from django.db.models import Count


class Tags(models.Model):
    """Модель для хранения тегов"""

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Questions(models.Model):
    """Модель для хранения вопросов"""

    class Meta:
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'

    title = models.CharField(max_length=50, verbose_name='Заголовок')
    body = models.TextField(verbose_name='Текст вопроса')
    author = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING
    )
    create_date = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tags)

    def __str__(self):
        return f'{self.title} {self.author.username}'

    @staticmethod
    def get_trends():
        return Questions.objects.annotate(count=Count('questionvotes')).order_by('-count')[:20]


class QuestionVotes(models.Model):
    """Модель для хранения голосов по вопросам"""

    class Meta:
        verbose_name = 'Question vote'
        verbose_name_plural = 'Question votes'

    author = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING
    )
    create_date = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(
        Questions,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Question votes by {self.author.username}"


class Answers(models.Model):
    """Модель для хранения ответов к вопросам"""

    class Meta:
        verbose_name = 'Answer'
        verbose_name_plural = 'Answers'

    body = models.TextField(max_length=1000, verbose_name='Ваш ответ')
    author = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING
    )
    create_date = models.DateTimeField(auto_now_add=True)
    correct = models.BooleanField(blank=True)
    question = models.ForeignKey(
        Questions,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'Answer of {self.author.username} from {self.create_date}'


class AnswerVotes(models.Model):
    """Модель для хранения голосов по ответам"""
    class Meta:
        verbose_name = 'Answer vote'
        verbose_name_plural = 'Answer votes'

    author = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING
    )
    create_date = models.DateTimeField(auto_now_add=True)
    answer = models.ForeignKey(
        Answers,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"Answer votes by {self.author.username}"
