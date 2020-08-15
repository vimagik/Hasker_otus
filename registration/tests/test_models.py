from django.test import TestCase
from django.contrib.auth.models import User

from registration.models import UserProfile


class UserProfileModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username='test_user'
        )
        UserProfile.objects.create(
            user=user,
        )

    def test_user_profile_user_label(self):
        profile = UserProfile.objects.get(id=1)
        user_label = profile._meta.get_field('user').verbose_name
        self.assertEqual(user_label, 'user')

    def test_user_profile_photo_label(self):
        profile = UserProfile.objects.get(id=1)
        photo_label = profile._meta.get_field('photo').verbose_name
        self.assertEqual(photo_label, 'photo')

    def test_user_str(self):
        profile = UserProfile.objects.get(id=1)
        self.assertEqual(str(profile), 'Profile of test_user')
