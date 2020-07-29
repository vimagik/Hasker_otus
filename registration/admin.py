from django.contrib import admin
from registration.models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', '__str__')
    empty_value_display = 'not stated'



