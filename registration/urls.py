from django.urls import path
from django.contrib.auth.decorators import login_required

from registration.views import *

app_name = 'registration'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('registration/', CreateUserView.as_view(), name='registration'),
    path('editprofile/', login_required(EditProfileView.as_view()), name='editprofile'),
]
