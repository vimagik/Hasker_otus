from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import User

from registration.forms import UserForm, UserProfileForm
from registration.models import UserProfile
from questions.views import get_trends


class Login(TemplateView):
    template_name = 'registration/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        get_trends(context)
        return context

    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect("/")
        else:
            return render(request, self.template_name, {'error': 'Не найдена пара логин-пароль'})


class Logout(LogoutView):
    next_page = '/'


class CreateUserView(TemplateView):
    template_name = 'registration/createUser.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserForm()
        get_trends(context)
        return context

    def post(self, request):
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            new_user = User(
                username=form.cleaned_data['login'],
                email=form.cleaned_data['email'],
            )
            new_user.set_password(form.cleaned_data['password1'])
            new_user.save()
            new_user_profile = UserProfile(
                photo=form.cleaned_data['photo'],
                user=new_user,
            )
            new_user_profile.save()
            return HttpResponseRedirect('/')
        return render(request, self.template_name, {'form': form})


class EditProfileView(TemplateView):
    template_name = 'registration/editProfile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserProfileForm()
        get_trends(context)
        return context

    def collect_data(self, request):
        data = {}
        photo_url = None
        if request.user.is_authenticated:
            data['login'] = request.user.username
            data['email'] = request.user.email
            profile = UserProfile.objects.filter(user=request.user)
            if profile is not None:
                photo_url = profile[0].photo.url
        context = {
            'form': UserProfileForm(initial=data),
            'photo_url': photo_url,
        }
        get_trends(context)
        return context

    def get(self, request, *args, **kwargs):
        context = self.collect_data(request)
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserProfileForm(request.POST, request.FILES)
        renewal = False
        if form.is_valid():
            email = form.cleaned_data['email']
            if email != request.user.email:
                request.user.email = email
                request.user.save()
                renewal = True
            photo = form.cleaned_data['photo']
            if photo:
                profile = UserProfile.objects.get(user=request.user)
                profile.photo = photo
                profile.save()
                renewal = True
        context = self.collect_data(request)
        if renewal:
            context['success'] = "Профиль обновлен"
        else:
            context['important'] = "Нет данных для обновления"
        return render(request, self.template_name, context)
