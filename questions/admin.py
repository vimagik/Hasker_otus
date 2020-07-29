from django.contrib import admin
from questions.models import *


@admin.register(Tags)
class TagsAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')


@admin.register(Answers)
class AnswersAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'correct')


@admin.register(QuestionVotes)
class AnswersAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'create_date')


@admin.register(AnswerVotes)
class AnswersAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__', 'create_date')
