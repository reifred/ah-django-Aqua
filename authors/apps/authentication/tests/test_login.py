from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .app_urls import register_url, login_url, activate_url, user_action_url
from .test_data import valid_user, valid_user2
from ..models import User


class LoginAPIViewTestCase(TestCase):
    """ This class defines the test suite for the login view. """

    def setUp(self):
        self.existing_user = User.objects.create_user(
            **valid_user)
        self.client = APIClient()

    def test_api_cannot_login_an_unregistered_user(self):
        response = self.client.post(
            login_url, {"user": valid_user2}, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'User not found or account not active.',
            response.data["errors"]['error'])

    def test_api_login_registered_user(self):
        response = self.client.post(
            register_url, {"user": valid_user2}, format="json")

        self.token = response.data["data"]["token"]

        self.client.get(f"{activate_url}?token={self.token}", format='json')

        response = self.client.post(
            login_url, {"user": valid_user2}, format="json")
            
        self.assertEqual(response.status_code, status.HTTP_200_OK)
