from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from authors.apps.authentication.models import User
from .test_data import valid_user, valid_user2

class ProfileFollowAPIViewTestCase(TestCase):

    def setUp(self):        
        user1 = User.objects.create_user(**valid_user)
        user2 = User.objects.create_user(**valid_user2)
        user2.is_active = True
        user2.save()

        self.client = APIClient()
        self.client.force_authenticate(user=user1)


    def test_un_authenticated_user_cannot_follow_or_unfollow_others(self):
        self.client.logout()
        response = self.client.post(
            '/api/profiles/peter/follow/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_un_authenticated_user_cannot_manage_followers(self):
        self.client.logout()
        response = self.client.get(
            '/api/profiles/peter/following/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_cannot_follow_non_existent_profile(self):
        response = self.client.post(
            '/api/profiles/fred/follow/'
        )
        self.assertIn(
            "The requested profile does not exist.",
            response.data["errors"]["detail"])

    def test_authenticated_user_can_follow_another_user(self):
        response = self.client.post(
            '/api/profiles/peter/follow/'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authenticated_user_cannot_re_follow_the_same_user(self):
        response = self.client.post(
            '/api/profiles/peter/follow/'
        )

        response = self.client.post(
            '/api/profiles/peter/follow/'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authenticated_user_cannot_follow_themselves(self):
        response = self.client.post(
            '/api/profiles/henryjones/follow/'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authenticated_user_can_unfollow_users_they_follow(self):
        response = self.client.post(
            '/api/profiles/peter/follow/'
        )
        response = self.client.delete(
            '/api/profiles/peter/follow/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_cannot_unfollow_users_they_are_not_following(self):
        response = self.client.delete(
            '/api/profiles/peter/follow/'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authenticated_user_cannot_unfollow_non_existent_profile(self):
        response = self.client.delete(
            '/api/profiles/fred/follow/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_user_cannot_see_followers_of_invalid_account(self):
        response = self.client.get(
            '/api/profiles/fred/following/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_users_cannot_see_followers_of_another_user(self):
        response = self.client.get(
            '/api/profiles/peter/following/'
        )
        self.assertIn(
            "Only account owners can see their followers and followees",
            response.data["errors"])
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_authenticated_users_can_see_their_followers_and_followees(self):
        response = self.client.get(
            '/api/profiles/henryjones/following/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
