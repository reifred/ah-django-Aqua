from django.test import TestCase

from .test_data import valid_user

from ..models import User


class UserTestCase(TestCase):
    """ This class defines the test suite for the user model. """

    def setUp(self):
        self.user = User(**valid_user)

    def test_model_can_create_a_user(self):
        previous_count = User.objects.count()
        self.user.save()
        current_count = User.objects.count()

        self.assertNotEqual(previous_count, current_count)
        self.assertEqual(str(self.user), self.user.email)

    def test_model_returns_fullname_of_user(self):
        self.user.save()
        self.assertEqual(self.user.get_full_name, self.user.username)

    def test_model_returns_shortname_of_user(self):
        self.user.save()
        self.assertEqual(self.user.get_short_name(), self.user.username)
