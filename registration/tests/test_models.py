import factory
from django.test import TestCase
from django.contrib.auth.models import User

from registration.models import UserProfile


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User


class UserProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserProfile


class UserProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = UserFactory(username='test_user')
        UserProfileFactory(user=user)

    def test_user_profile_user_label(self):
        profile = UserProfile.objects.get(user__username='test_user')
        user_label = profile._meta.get_field('user').verbose_name
        self.assertEqual(user_label, 'user')

    def test_user_profile_photo_label(self):
        profile = UserProfile.objects.get(user__username='test_user')
        photo_label = profile._meta.get_field('photo').verbose_name
        self.assertEqual(photo_label, 'photo')

    def test_user_str(self):
        profile = UserProfile.objects.get(user__username='test_user')
        self.assertEqual(str(profile), 'Profile of test_user')
