from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from authors.apps.articles.models import Article
from authors.apps.articles.tests.test_data import (
    valid_article, valid_article_2, slug,
    signup_and_login_user
    )
from authors.apps.authentication.models import User
from authors.apps.authentication.tests.test_data import (
    valid_user,valid_user2)
from authors.apps.authentication.tests.app_urls import *


class LikeDislikeAPIViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

        signup_and_login_user(User, valid_user, self.client)
        self.client.post(
            '/api/articles/',
            {"article":valid_article_2},
            format="json"
        )

    def test_unauthenticated_user_cannot_like_article(self):
        self.client.logout()
        response = self.client.post(
            f'/api/articles/{slug}/like/',
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unauthenticated_user_cannot_dislike_article(self):
        self.client.logout()
        response = self.client.post(
            f'/api/articles/{slug}/dislike/',
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cant_like_a_non_existent_article(self):
        response = self.client.post(
            f'/api/articles/like-dislike/how-to-so-good/',
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_authenticated_user_can_like_article(self):
        self.client.logout()
        signup_and_login_user(User,valid_user2,self.client)
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
        self.assertEqual(response.data['likes'], True)


    def test_authenticated_user_can_dislike_an_article(self):
        self.client.logout()
        signup_and_login_user(User,valid_user2,self.client)
        article = (Article.objects.all()[0])
        response = self.client.post(
            reverse(
                'articles:dislikes',
                kwargs={
                    "slug": article.slug
                }
            ),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['likes'], False)

    def test_user_can_dislike_an_article_more_than_once_but_with_one_dilike(
        self
        ):
        self.client.logout()
        signup_and_login_user(User,valid_user2,self.client)
        article = (Article.objects.all()[0])
        self.client.post(
            reverse(
                'articles:dislikes',
                kwargs={
                    "slug": article.slug
                }
            ),
            format='json'
        )
        response = self.client.post(
            reverse(
                'articles:dislikes',
                kwargs={
                    "slug": article.slug
                }
            ),
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['likes'], False)
        self.assertEqual(article.likes,0)

    def user_can_like_more_than_once_with_one_like_still(self):
        self.client.logout()
        signup_and_login_user(User,valid_user2,self.client)
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
        self.assertEqual(response.data['likes'], True)
        self.assertEqual(len(response.data['likes']),1)
        self.assertEqual(article.likes,1)
