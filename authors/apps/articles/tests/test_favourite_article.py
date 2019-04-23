from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from authors.apps.articles.models import Article
from authors.apps.authentication.models import User
from authors.apps.authentication.tests.test_data import valid_user
from authors.apps.articles.tests.test_data import valid_article

class FavoriteArticleAPIViewTestCase(TestCase):

    def setUp(self):        
        user = User.objects.create_user(**valid_user)
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.client.post('/api/articles/',
            {"article": valid_article}, format="json")

    def test_un_authenticated_user_cannot_favourite_an_article(self):
        self.client.logout()
        response = self.client.post(
            '/api/articles/how-to-train-your-dragon/favourite/',
            {"article": valid_article},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_un_authenticated_user_cannot_un_favourite_an_article(self):
        self.client.logout()
        response = self.client.delete(
            '/api/articles/how-to-train-your-dragon/favourite/',
            {"article": valid_article},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_authenticated_user_can_favourite_an_article(self):
        response = self.client.post(
            '/api/articles/how-to-train-your-dragon/favourite/',
            {"article": valid_article},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_authenticated_user_can_un_favourite_an_article(self):
        response = self.client.delete(
            '/api/articles/how-to-train-your-dragon/favourite/',
            {"article": valid_article},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_cannot_favourite_non_existent_article(self):
        response = self.client.post(
            '/api/articles/how-to-train-your-car/favourite/',
            {"article": valid_article},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_user_cannot_un_favourite_non_existent_article(self):
        response = self.client.delete(
            '/api/articles/how-to-train-your-car/favourite/',
            {"article": valid_article},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_favourite_count_of_an_article(self):
        self.client.post(
            '/api/articles/how-to-train-your-dragon/favourite/',
            {"article": valid_article},
            format="json"
        )
        article = Article.objects.get(slug='how-to-train-your-dragon')
        current_favourite_count = article.favourited_by.count()
        expected_favourite_count = 1
        self.assertEqual(current_favourite_count, expected_favourite_count)

