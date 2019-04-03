from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .app_urls import(
    register_url, reset_password_url, login_url,
    new_passord_url, activate_url
)

from .test_data import valid_user, invalid_token, expired_token


class RequestNewPasswordTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Register a user
        response = self.client.post(
            register_url, {"user": valid_user}, format="json")

    def test_user_reset_password_with_no_email_field(self):
        response = self.client.post(reset_password_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Email field required to reset password", response.data["errors"])

    def test_user_reset_password_with_valid_email(self):
        response = self.client.post(
            reset_password_url, {"email": "hjones@email.com"}, 
            format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn(
            "Please check your email for recovery password link.", 
            response.data["message"])

    def test_user_change_password_with_no_password_field(self):
        response = self.client.patch(new_passord_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Password field required to change password", 
            response.data["errors"])

    def test_user_change_password_with_less_password_length(self):
        response = self.client.patch(
            new_passord_url, {"password": "fred"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Password length must be greater than 7 characters", 
            response.data["errors"])

    def test_user_change_password_with_expired_verification_link(self):
        response = self.client.patch(
            f"{new_passord_url}?token={expired_token}", 
            {"password": "Pass1234"}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_change_password_with_invalid_verification_link(self):
        response = self.client.patch(
            f"{new_passord_url}?token={invalid_token}", 
            {"password": "Pass1234"}, format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "Verifcation link is invalid. Check email for correct link.", 
            response.data["detail"])
