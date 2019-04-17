from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from authors.apps.articles.models import Article
from authors.apps.articles.tests.test_data import new_valid_article
from authors.apps.authentication.models import User
from authors.apps.authentication.tests.test_data import valid_user3, valid_user4


class DestroyArticleAPIViewTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(**valid_user3)
        self.user2 = User.objects.create_user(**valid_user4)

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.data = new_valid_article

    def test_api_can_delete_an_article_with_authenticated_user(self):

        article = self.data
        
        self.client.force_authenticate(user=self.user)

        self.client.post(
            '/api/articles/',
            {"article": article},
            format="json"
        )
        response = self.client.delete(
            '/api/articles/how-to-train-your-robot/'
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_api_can_not_delete_an_article_with_unauthenticated_user(self):
        article = self.data
        self.client.post(
            '/api/articles/',
            {"article": article},
            format="json"
        )
        self.client.logout()
        response = self.client.delete(
            '/api/articles/how-to-train-your-robot/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_can_not_delete_an_article_with_unknown_slug(self):
        article = self.data
        self.client.post(
            '/api/articles/',
            {"article": article},
            format="json"
        )
        response = self.client.delete(
            '/api/articles/how-to-train-your-robot-2/'
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_api_cannot_delete_an_article_with_an_article_non_creator_user(self):

        article = self.data
        self.client.post(
            '/api/articles/',
            {"article": article},
            format="json"
        )
        self.client.logout()
        self.client.force_authenticate(user=self.user2)

        response = self.client.delete(
            '/api/articles/how-to-train-your-robot/'
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
