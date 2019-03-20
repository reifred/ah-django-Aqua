from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import User, UserManager


class UserTestCase(TestCase):
    """ This class defines the test suite for the user model. """

    def setUp(self):
        self.username = "henryjones"
        self.email = "hjones@email.com"
        self.password = "T35ting-i2E"
        self.user = User(username=self.username, email=self.email, password=self.password)

    def test_model_can_create_a_user(self):
        fields = [
            self.username,
            self.email,
            self.password
        ]

        previous_count = User.objects.count()
        self.user.save()
        current_count = User.objects.count()

        self.assertNotEqual(previous_count, current_count)
        self.assertIn(self.user.username, fields)
        self.assertIn(self.user.email, fields)
        self.assertIn(self.user.password, fields)
    
    def test_model_returns_fullname_of_user(self):
        self.user.save()

        self.assertEqual(self.user.get_full_name, self.username)

    def test_model_returns_shortname_of_user(self):
        self.user.save()

        self.assertEqual(self.user.get_short_name(), self.username)
    
class  UserManagerTestCase(TestCase):
    """ This class defines the test suite for the user manager model. """
    
    def setUp(self):
        self.username = "henryjones"
        self.email = "hjones@email.com"
        self.password = "T35ting-i2E"

    def test_manager_can_create_a_regular_user_with_required_fields(self):
        kwargs = {
            "username": self.username,
            "email": self.email,
            "password": self.password
        }
        
        previous_count = User.objects.count()
        user = User.objects.create_user(**kwargs)
        current_count = User.objects.count()

        self.assertNotEqual(previous_count, current_count)
        self.assertFalse(user.is_superuser)
    
    def test_manager_can_create_a_regular_user_without_password_field(self):
        kwargs = {
            "username": self.username,
            "email": self.email
        }

        user = User.objects.create_user(**kwargs)
        self.assertIsNotNone(user.password)
        self.assertFalse(user.is_superuser)
    
    def test_manager_cannot_create_a_regular_user_without_username_field(self):
        kwargs = {
            "email": self.email,
            "password": self.password
        }

        self.assertRaises(TypeError, User.objects.create_user, **kwargs)
    
    def test_manager_cannot_create_a_regular_user_without_email_field(self):
        kwargs = {
            "username": self.username,
            "password": self.password
        }

        self.assertRaises(TypeError, User.objects.create_user, **kwargs)
    
    def test_manager_can_create_a_super_user_with_required_fields(self):
        kwargs = {
            "username": self.username,
            "email": self.email,
            "password": self.password
        }

        previous_count = User.objects.count()
        user = User.objects.create_superuser(**kwargs)
        current_count = User.objects.count()

        self.assertNotEqual(previous_count, current_count)
        self.assertTrue(user.is_superuser)
    
    def test_manager_cannot_create_a_super_user_without_username_field(self):
        kwargs = {
            "email": self.email,
            "password": self.password
        }

        self.assertRaises(TypeError, User.objects.create_superuser, **kwargs)
    
    def test_manager_cannot_create_a_super_user_without_email_field(self):
        kwargs = {
            "username": self.username,
            "password": self.password
        }

        self.assertRaises(TypeError, User.objects.create_superuser, **kwargs)

    def test_manager_cannot_create_a_super_user_without_password_field(self):
        kwargs = {
            "username": self.username,
            "email": self.email
        }

        self.assertRaises(TypeError, User.objects.create_superuser, **kwargs)
    

class RegistrationAPIViewTestCase(TestCase):
    """ This class defines the test suite for the registration view. """
    
    def setUp(self):
        
        self.existing_user_data= {
            "username": "janejones",
            "email": "jjones@email.com",
            "password": "Enter-123"
        }
        self.existing_user = User.objects.create_user(**self.existing_user_data)
        self.client = APIClient()
    
    def test_api_can_create_a_user(self):

        user_data = {
            "username": "henryjones",
            "email": "hjones@email.com",
            "password": "Enter-123"
        }

        response = self.client.post(
            '/api/users/',
            { "user": user_data},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_api_cannot_create_a_user_with_existing_email(self):

        user_data = {
            "username": "peter",
            "email": self.existing_user_data["email"],
            "password": "Enter123"
        }

        response = self.client.post(
            '/api/users/',
            { "user": user_data},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("user with this email already exists.", response.data["errors"]["email"], )
    
    def test_api_cannot_create_a_user_with_existing_username(self):

        user_data = {
            "username": self.existing_user_data["username"],
            "email": "peter@email.com",
            "password": "Enter123"
        }

        response = self.client.post(
            '/api/users/',
            { "user": user_data},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("user with this username already exists.", response.data["errors"]["username"])
    
    def test_api_cannot_create_a_user_with_password_lessthan_eight_characters(self):

        user_data = {
            "username": "peter",
            "email": "peter@email.com",
            "password": "Enter"
        }

        response = self.client.post(
            '/api/users/',
            { "user": user_data},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Ensure this field has at least 8 characters.", response.data["errors"]["password"])

class LoginAPIViewTestCase(TestCase):
    """ This class defines the test suite for the login view. """

    def setUp(self):

        self.existing_user_data= {
            "username": "janejones",
            "email": "jjones@email.com",
            "password": "Enter-123"
        }
        self.existing_user = User.objects.create_user(**self.existing_user_data)
        self.client = APIClient()

    def test_api_can_login_a_registered_user(self):

        pass



