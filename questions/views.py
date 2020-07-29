from django.shortcuts import render, HttpResponse
from registration.models import UserProfile


def index(request):
    context = {}
    if request.user.is_authenticated:
        profile = UserProfile.objects.filter(user=request.user)
        context['photo'] = profile[0].photo
    return render(request, 'questions/index.html', context)
