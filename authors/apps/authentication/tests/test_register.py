from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .app_urls import register_url
from .test_data import (
    valid_user, valid_user2,
    user_with_existing_email, user_with_existing_username,
    user_with_little_password,
    user_with_a_non_numeric_password,
    username_with_special_characters,
    invalid_email,
    user_with_short_username,
    message,
    user_with_existing_email,
    user_with_existing_username,
    user_with_little_password
    )

from ..models import User


class RegistrationAPIViewTestCase(TestCase):
    """ This class defines the test suite for the registration view. """

    def setUp(self):
        self.existing_user = User.objects.create_user(
            **valid_user)
        self.client = APIClient()

    def test_api_can_create_a_user(self):
        response = self.client.post(
            register_url, {"user": valid_user2}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_cannot_create_a_user_with_existing_email(self):
        response = self.client.post(
            register_url, 
            {"user": user_with_existing_email}, 
            format="json"
            )

        self.assertEqual(
            response.status_code, 
            status.HTTP_400_BAD_REQUEST
            )
        self.assertIn("user with this email already exists.",
                      response.data["errors"]["email"], )

    def test_api_cannot_create_a_user_with_existing_username(self):
        response = self.client.post(
            register_url, 
            {"user": user_with_existing_username}, 
            format="json"
            )

        self.assertEqual(
            response.status_code, 
            status.HTTP_400_BAD_REQUEST
            )
        self.assertIn("user with this username already exists.",
                      response.data["errors"]["username"])

    def test_api_cannot_create_a_user_with_password_lessthan_eight_characters(
                                                                    self):
        response = self.client.post(
            register_url,
            {"user": user_with_little_password}, 
            format="json"
            )

        self.assertEqual(
            response.status_code, 
            status.HTTP_400_BAD_REQUEST
            )
        self.assertIn("Ensure this field has at least 8 characters.",
                      response.data["errors"]["password"])

    def test_api_cannot_create_user_without_alphanumeric_password(self):
        response = self.client.post(
            register_url,
            { "user": user_with_a_non_numeric_password},
            format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            "password must contain a numeric character", 
            response.data["errors"]["password"]
            )

    def test_api_cannot_create_user_with_invalid_email(self):
        response = self.client.post(
            register_url,
            { "user": invalid_email},
            format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Enter a valid email address.", 
        response.data["errors"]["email"])


    def test_api_cannot_create_user_with_short_username(self):
        response = self.client.post(
            register_url,
            { "user": user_with_short_username},
            format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            message, 
            response.data["errors"]["username"])


    def test_api_cannot_create_user_with_special_character_in_username(self):
        response = self.client.post(
            register_url,
            { "user": username_with_special_characters},
            format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            message, 
            response.data["errors"]["username"])
