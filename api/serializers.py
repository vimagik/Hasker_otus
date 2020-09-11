from rest_framework import serializers

from questions.models import Questions


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Questions
        fields = ['title', 'body', 'create_date']
