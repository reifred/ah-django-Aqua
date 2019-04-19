from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from authors.apps.articles.models import Article
from authors.apps.articles.tests.test_data import (
    valid_article, valid_article_2
    )
from authors.apps.authentication.models import User
from authors.apps.authentication.tests.test_data import valid_user


class CreateArticleAPIViewTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(**valid_user)

        self.client = APIClient()
        self.client.force_authenticate(user=user)

        self.data = valid_article

    def test_api_can_create_an_article_with_authenticated_user(self):
        article = self.data

        response = self.client.post(
            '/api/articles/',
            {"article": article},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_cannot_create_an_article_with_an_unauthenticated_user(self):
        self.client.logout()

        article = self.data

        response = self.client.post(
            '/api/articles/',
            {"article": article},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_that_every_256_words_or_below_is_1_min_read(self):
        article = self.data

        response = self.client.post(
            '/api/articles/',
            {"article": article},
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('1 min read', response.data["read_time"])

    def test_that_a_word_over_256_words_increases_the_readtime(self):
        response = self.client.post(
            '/api/articles/',
            {"article": valid_article_2},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('2 min read', response.data["read_time"])
