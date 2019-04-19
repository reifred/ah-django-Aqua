from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from authors.apps.articles.models import Article
from authors.apps.articles.tests.test_data import (
    valid_article, valid_article_2, slug
    )
from authors.apps.authentication.models import User
from authors.apps.authentication.tests.test_data import (
    valid_user,valid_user2)
from authors.apps.authentication.tests.app_urls import *


class LikeDislikeAPIViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        response = self.client.post(
            register_url, {"user": valid_user}, format="json")

        self.token = response.data["data"]["token"]
        print(response.data)
        self.client.get(f"{activate_url}?token={self.token}", format='json')

        response = self.client.post(
            login_url, {"user": valid_user}, format='json')

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)

        self.client.post(
            '/api/articles/',
            {"article":valid_article_2},
            format="json"
        )

    def test_unauthenticated_user_cannot_like_or_dislike_article(self):
        self.client.logout()
        response = self.client.post(
            f'/api/articles/like-dislike/{slug}/',
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_one_cant_like_their_own_article(self):
        response = self.client.post(
            f'/api/articles/like-dislike/{slug}/',
            {"article":None},
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cant_like_a_non_existent_article(self):
        response = self.client.post(
            f'/api/articles/like-dislike/how-to-so-good/',
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_auth_user_can_like_article(self):
        self.client.post(
            '/api/articles/',
            {"article":valid_article_2},
            format="json"
        )
        self.client.logout()
        
        response = self.client.post(
            register_url, {"user":valid_user2}, format="json")

        self.token = response.data["data"]["token"]

        self.client.get(f"{activate_url}?token={self.token}", format='json')

        response = self.client.post(
            login_url, {"user": valid_user2}, format='json')

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        article = (Article.objects.all()[0])
        response = self.client.post(
            reverse(
                'articles:likes',
                kwargs={
                    "slug": article.slug
                }
            ),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['details']['likes'], True)


    def test_auth_user_can_dislike_an_article(self):
        self.client.post(
            '/api/articles/',
            {"article":valid_article_2},
            format="json"
        )
        self.client.logout()
        
        response = self.client.post(
            register_url, {"user":valid_user2}, format="json")

        self.token = response.data["data"]["token"]

        self.client.get(f"{activate_url}?token={self.token}", format='json')

        response = self.client.post(
            login_url, {"user": valid_user2}, format='json')

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token)
        article = (Article.objects.all()[0])
        self.client.post(
            reverse(
                'articles:likes',
                kwargs={
                    "slug": article.slug
                }
            ),
            format='json'
        )
        response = self.client.post(
            reverse(
                'articles:likes',
                kwargs={
                    "slug": article.slug
                }
            ),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['details']['likes'], False)
    