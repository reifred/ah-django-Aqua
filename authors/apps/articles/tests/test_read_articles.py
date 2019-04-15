from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from authors.apps.articles.models import Article
from authors.apps.articles.tests.test_data import (auth_error,
                                                   non_existent_slug,
                                                   not_found, slug,
                                                   valid_article)
from authors.apps.authentication.models import User
from authors.apps.authentication.tests.test_data import valid_user


class ReadArticlesAPIViewTestCase(TestCase):

    def setUp(self):
        user = User.objects.create_user(**valid_user)

        valid_article.update(
            {"author_id": user.id}
        )
        # create three articles in the test database
        COUNT = 3
        while COUNT != 0:
            article = Article(**valid_article)
            article.save()
            COUNT -= 1

        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def test_api_can_read_articles_with_authenticated_user(self):
        response = self.client.get(
            '/api/articles/',
        )
        # we expect only the three articles created at setUp
        # to be in our test database
        EXPECTED = 3

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), EXPECTED)

    def test_api_can_read_articles_with_an_unauthenticated_user(self):
        self.client.logout()

        response = self.client.get(
            '/api/articles/',
        )
        # we expect only the three articles created at setUp
        # to be in our test database
        EXPECTED = 3

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), EXPECTED)

    def test_api_can_read_an_article_with_authenticated_user(self):
        response = self.client.get(
            f'/api/articles/{slug}/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(slug, response.data['slug'])

    def test_api_can_read_an_article_with_an_unauthenticated_user(self):
        self.client.logout()

        response = self.client.get(
            f'/api/articles/{slug}/'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(slug, response.data['slug'])

    def test_api_returns_error_when_retrieving_non_existent_slug(self):
        response = self.client.get(
            f'/api/articles/{non_existent_slug}/'
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn(not_found, response.data['detail'])
