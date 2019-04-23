from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .test_data import (
    valid_user, profile_data, partial_profile_data)
from authors.apps.authentication.models import User


class UpdateProfilesTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(**valid_user)

        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def test_authenticated_user_can_update_their_profile(self):
        response = self.client.put(
            '/api/profiles/',
            profile_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, profile_data["profile"]["bio"])

    def test_authenticated_user_can_partially_update_their_profile(self):
        response = self.client.put(
            '/api/profiles/',
            partial_profile_data,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, partial_profile_data["profile"]["image"])

    def test_authentication_required_to_update_a_profile(self):
        self.client.logout()
        response = self.client.put(
            '/api/profiles/',
            partial_profile_data,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
