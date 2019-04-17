from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from authors.apps.articles.models import Article
from authors.apps.articles.tests.test_data import (
    valid_article, update_article_title
)
from authors.apps.authentication.models import User
from authors.apps.authentication.tests.test_data import valid_user


class UpdateArticleAPIViewTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(**valid_user)
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.client.post('/api/articles/',
            {"article": valid_article}, format="json")

    def test_api_can_update_an_article_with_authenticated_user(self):
        response = self.client.patch(
            '/api/articles/how-to-train-your-dragon/',
            {"article": update_article_title},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_cannot_update_an_article_with_an_unauthenticated_user(self):
        self.client.logout()

        response = self.client.patch(
            '/api/articles/how-to-train-your-dragon/',
            {"article": valid_article},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_cannot_update_an_inexistent_article(self):
        response = self.client.patch(
            '/api/articles/how-to-train-your-dragon2/',
            {"article": valid_article},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
