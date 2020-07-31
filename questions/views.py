from django.shortcuts import render, HttpResponse
from django.db.models import Count
from registration.models import UserProfile
from questions.models import QuestionVotes


def get_trends(context: dict):
    trends = QuestionVotes.objects.values('question__title').annotate(count=Count('question')).order_by('-count')[:20]
    context['trends'] = trends


def index(request):
    context = {}
    if request.user.is_authenticated:
        profile = UserProfile.objects.filter(user=request.user)
        context['photo'] = profile[0].photo
    get_trends(context)
    return render(request, 'questions/index.html', context)
