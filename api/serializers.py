from rest_framework import serializers

from questions.models import Questions, Answers


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    """Сериализатор для работы с Question"""
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )
    tags = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Questions
        fields = ['title', 'body', 'create_date', 'author', 'tags']


class TrendsSerializer(serializers.Serializer):
    """Сериализатор для трендов"""
    count = serializers.IntegerField()
    title = serializers.CharField(max_length=50)


class AnswerSerializer(serializers.HyperlinkedModelSerializer):
    """Сериализатор для ответов"""
    author = serializers.SlugRelatedField(
        many=False,
        read_only=True,
        slug_field='username'
    )

    class Meta:
        model = Answers
        fields = ['body', 'author', 'create_date', 'correct']
