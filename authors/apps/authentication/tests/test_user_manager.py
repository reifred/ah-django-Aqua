from django.test import TestCase

from .test_data import (
    valid_user, user_without_password,
    user_without_username, user_without_email,
    )

from ..models import User, UserManager

class UserManagerTestCase(TestCase):
    """ This class defines the test suite for the user manager model. """

    def test_manager_can_create_a_regular_user_with_required_fields(self):
        previous_count = User.objects.count()
        user = User.objects.create_user(**valid_user)
        current_count = User.objects.count()

        self.assertNotEqual(previous_count, current_count)
        self.assertFalse(user.is_superuser)

    def test_manager_can_create_a_regular_user_without_password_field(self):
        user = User.objects.create_user(**user_without_password)
        self.assertIsNotNone(user.password)
        self.assertFalse(user.is_superuser)

    def test_manager_cannot_create_a_regular_user_without_username_field(self):
        self.assertRaises(TypeError, User.objects.create_user, **user_without_username)

    def test_manager_cannot_create_a_regular_user_without_email_field(self):
        self.assertRaises(TypeError, User.objects.create_user, user_without_email)

    def test_manager_can_create_a_super_user_with_required_fields(self):
        previous_count = User.objects.count()
        user = User.objects.create_superuser(**valid_user)
        current_count = User.objects.count()

        self.assertNotEqual(previous_count, current_count)
        self.assertTrue(user.is_superuser)

    def test_manager_cannot_create_a_super_user_without_username_field(self):
        self.assertRaises(TypeError, User.objects.create_superuser, **user_without_username)

    def test_manager_cannot_create_a_super_user_without_email_field(self):
        self.assertRaises(TypeError, User.objects.create_superuser, **user_without_email)

    def test_manager_cannot_create_a_super_user_without_password_field(self):
        self.assertRaises(TypeError, User.objects.create_superuser, **user_without_password)
