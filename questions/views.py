from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count
from django.views.generic import TemplateView, DetailView, RedirectView, ListView
from registration.models import UserProfile
from questions.models import QuestionVotes, Questions, Tags, Answers, AnswerVotes
from django.core.mail import send_mail

from questions.forms import QuestionCreateForm, AnswerCreateForm


def get_trends(context: dict):
    trends = Questions.objects.annotate(count=Count('questionvotes')).order_by('-count')[:20]
    context['trends'] = trends


class IndexView(ListView):
    model = Questions
    template_name = 'questions/index.html'
    paginate_by = 20

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.request.user.is_authenticated:
            profile = UserProfile.objects.get(user=self.request.user)
            context['photo'] = profile.photo
        if self.request.session.get('order') == 'date':
            context['order_date'] = 'active'
        else:
            context['order_popular'] = 'active'
        get_trends(context)
        return context

    def get_queryset(self):
        if self.request.GET.get('order'):
            self.request.session['order'] = self.request.GET['order']
        elif self.request.session.get('order') is None:
            self.request.session['order'] = 'popular'
        if self.request.session.get('order') == 'date':
            order = '-create_date'
        elif self.request.session.get('order') == 'popular':
            order = '-count_votes'
        queryset = Questions.objects.annotate(
            count_votes=Count('questionvotes', distinct=True),
            count_answers=Count('answers', distinct=True)
        ).order_by(order)
        return queryset


class CreateQuestionView(TemplateView):
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
            return redirect(f'/question/{new_question.id}/')
        return render(request, self.template_name, {'form': form})


class QuestionView(ListView):
    model = Answers
    template_name = 'questions/question_detail.html'
    paginate_by = 2

    def get_queryset(self):
        self.question = get_object_or_404(Questions, pk=self.kwargs.get('pk'))
        queryset = Answers.objects.filter(question=self.question).annotate(count=Count('answervotes')).order_by('-count', '-create_date')
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        number_question_votes = QuestionVotes.objects.filter(question=self.question).count()
        context['number_question_votes'] = number_question_votes
        context['question'] = self.question
        if self.request.user.is_authenticated:
            if self.request.user != self.question.author:
                context['disabled_correct_answer'] = 'disabled'
        else:
            context['disabled_correct_answer'] = 'disabled'
            context['disabled'] = 'disabled'
        form = AnswerCreateForm()
        context['form'] = form
        get_trends(context)
        return context

    def post(self, request, pk):
        form = AnswerCreateForm(request.POST)
        if form.is_valid():
            new_answer = Answers(
                body=form.cleaned_data['body'],
                author=request.user,
                question=Questions.objects.get(id=pk),
                correct=False,
            )
            new_answer.save()
            send_mail(
                subject='Получен ответ на ваш вопрос',
                message=f'Ссылка на ваш вопрос ',
                from_email='info@homework.ru',
                recipient_list=[request.user.email],
                fail_silently=True,
            )
        return redirect(f'/question/{pk}')


class QuestionVoteView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs['pk']
        new_vote, created = QuestionVotes.objects.get_or_create(
            author=self.request.user,
            question_id=pk
        )
        if created:
            new_vote.save()
        current_page = self.request.GET.get('page')
        self.url = f"/question/{pk}/?page={current_page}"
        return super().get_redirect_url(*args, **kwargs)


class QuestionUnVoteView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs['pk']
        vote = QuestionVotes.objects.filter(
            author=self.request.user,
            question_id=pk
        ).first()
        if vote:
            vote.delete()
        current_page = self.request.GET.get('page')
        self.url = f"/question/{pk}/?page={current_page}"
        return super().get_redirect_url(*args, **kwargs)


class AnswerVoteView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs['pk']
        id_answer = kwargs['id_answer']
        new_vote_answer, created = AnswerVotes.objects.get_or_create(
            author=self.request.user,
            answer_id=id_answer
        )
        if created:
            new_vote_answer.save()
        current_page = self.request.GET.get('page')
        self.url = f"/question/{pk}/?page={current_page}"
        return super().get_redirect_url(*args, **kwargs)


class AnswerUnVoteView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs['pk']
        id_answer = kwargs['id_answer']
        vote_answer = AnswerVotes.objects.filter(
            author=self.request.user,
            answer_id=id_answer
        ).first()
        if vote_answer:
            vote_answer.delete()
        current_page = self.request.GET.get('page')
        self.url = f"/question/{pk}/?page={current_page}"
        return super().get_redirect_url(*args, **kwargs)


class AnswerSelectRightView(RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        pk = kwargs['pk']
        current_question = Questions.objects.get(pk=pk)
        if self.request.user != current_question.author:
            return super().get_redirect_url(*args, **kwargs)
        id_answer = kwargs['id_answer']
        old_correct_answer = Answers.objects.filter(correct=True).first()
        if old_correct_answer:
            old_correct_answer.correct = False
            old_correct_answer.save()
        answer = Answers.objects.get(pk=id_answer)
        answer.correct = True
        answer.save()
        current_page = self.request.GET.get('page')
        self.url = f"/question/{pk}/?page={current_page}"
        return super().get_redirect_url(*args, **kwargs)
