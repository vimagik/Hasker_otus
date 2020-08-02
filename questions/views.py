from django.shortcuts import render, HttpResponse
from django.db.models import Count
from django.views.generic import TemplateView
from registration.models import UserProfile
from questions.models import QuestionVotes, Questions, Tags

from questions.forms import QuestionCreateForm


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


class NewQuestionView(TemplateView):
    template_name = 'questions/newQuestion.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = QuestionCreateForm()
        get_trends(context)
        return context

    def post(self, request):
        form = QuestionCreateForm(request.POST)
        if form.is_valid():
            new_question = Questions(
                title=form.cleaned_data['title'],
                body=form.cleaned_data['body'],
                author=request.user
            )
            new_question.save()
            for tag in form.cleaned_data['tags'].split(','):
                new_tag, _ = Tags.objects.get_or_create(
                    name=tag
                )
                new_question.tags.add(new_tag)
            return HttpResponse('Форма успшено сохранена')
        return render(request, self.template_name, {'form': form})
