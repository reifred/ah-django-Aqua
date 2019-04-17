from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .app_urls import register_url, login_url, activate_url, user_action_url
from .test_data import (
    valid_user, 
    invalid_token, 
    user_data_2,
    profiles
    )


class UserRetrieveUpdateAPIViewTestCase(TestCase):
    """
    This class defines the test suite for the view
    that retrieves and updates a user
    """

    def setUp(self):
        self.client = APIClient()

        response = self.client.post(
            register_url, {"user": valid_user}, format="json")
        response = self.client.post(
            register_url, {"user": user_data_2}, format="json")

        self.token = response.data["data"]["token"]

        self.client.get(f"{activate_url}?token={self.token}", format='json')

        response = self.client.post(
            login_url, {"user": valid_user}, format='json')

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

    def test_verify_account_with_invalid_token(self):
        self.client.get(f"{activate_url}?token={invalid_token}", format='json')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + invalid_token)
        response = self.client.get(user_action_url, format="json")
        self.assertIn(
            "Invalid authentication. Could not decode token.",
            response.data["errors"]["detail"])

    def test_invalid_verification_link(self):
        response = self.client.get(
            f"{activate_url}?token={invalid_token}", format='json'
            )
        self.assertIn(
            "Verifcation link is invalid. Check email for correct link.",
            response.data["errors"]["detail"])

    def test_api_can_retrieve_a_registered_user(self):

        response = self.client.get(user_action_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_needs_authentication_to_retrieve_a_user(self):

        self.client.logout()

        response = self.client.get(user_action_url, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_can_update_user_data(self):

        new_user_data = {
            "email": "jjones@email.com",
            "bio": "I like eggs for breakfast",
            "image": "https://myimages.com/erwt.png"}

        response = self.client.put(
            user_action_url, {"user": new_user_data}, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_needs_authentication_to_update_user_data(self):
        new_user_data = {
            "email": "jjones@email.com",
            "bio": "I like eggs for breakfast",
            "image": "https://myimages.com/erwt.png"}

        self.client.logout()

        response = self.client.put(
            user_action_url, {"user": new_user_data}, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_get_user_data_with_bad_authorization_header(self):
        response = self.client.post(
            login_url, {"user": valid_user}, format='json')

        self.client.credentials(HTTP_AUTHORIZATION='Fred ' + self.token)
        response = self.client.get(login_url, format="json")
        self.assertIn(
            "Bad Authorization header.", 
            response.data["errors"]["detail"]
            )

    def test_api_get_user_data_with_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + invalid_token)
        response = self.client.get(user_action_url, format="json")
        self.assertIn(
            "Invalid authentication. Could not decode token.",
            response.data["errors"]["detail"])

    def test_api_can_allow_user_to_view_another_person_status(self):
        response = self.client.get(
            '/api/profiles/nicksbro/',
            format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("nicksbro", response.data["username"])

    def test_profile_created_on_user_registration(self):
        response = self.client.get(
            '/api/profiles/nicksbro/',
            format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("", response.data["username"])
        self.assertIn("", response.data["image"])

    def test_api_cannot_retrieve_a_non_existing_profile(self):
        response = self.client.get(
            '/api/profiles/jane/',
            format="json")

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn(
            "The requested profile does not exist.",
            response.data["errors"]["detail"])

    def test_api_user_cannot_update_other_persons_profiles(self):
        new_user_data = {
            "email": "jjones@email.com",
            "bio": "I like eggs for breakfast",
            "image": "https://myimages.com/erwt.png"}
        response = self.client.put(
            '/api/profiles/nicksbro/',
            {"user": new_user_data},
            format="json")

        self.assertEqual(
            response.status_code, 
            status.HTTP_405_METHOD_NOT_ALLOWED
            )

    def test_user_can_view_their_own_status(self):
        response = self.client.get(
            '/api/user/',
            format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_non_authenticated_user_cant_see_a_list_of_profiles(self):
        self.client.logout()
        response = self.client.get(
            profiles,
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn(
            "Authentication credentials were not provided.", 
            response.data['detail']
            )

    def test_authenticated_user_can_retrieve_all_profiles(self):
        response = self.client.get(
            profiles,
        )
        user_profiles_expected = 2
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data),user_profiles_expected)
