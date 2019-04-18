from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from authors.apps.articles.models import Article, Ratings
from authors.apps.articles.tests.test_data import (
    valid_article, valid_article_2,
    valid_rating, slug, invalid_rating, valid_rating_2, 
    invalid_rating2, invalid_integer, 
    signup_and_login_user
    )
from authors.apps.authentication.models import User
from authors.apps.authentication.tests.test_data import (
    valid_user, valid_user2
    )
from authors.apps.authentication.tests.app_urls import (
    register_url, login_url, activate_url, user_action_url
    )


class RateArticleAPIViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        signup_and_login_user(User,valid_user,self.client)
        self.client.post('/api/articles/',
            {"article": valid_article}, format="json")
        
    def test_user_without_authentication_cant_rate_article(self):
        self.client.logout()
        response = self.client.post(
            f'/api/articles/{slug}/rate/',
            valid_rating,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_unathenticated_user_can_see_ratings(self):
        self.client.logout()
        response = self.client.get(
            f'/api/articles/{slug}/rate/',
            valid_rating,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(slug, response.data['slug'])

    def test_athenticated_user_can_see_ratings(self):
        response = self.client.get(
            f'/api/articles/{slug}/rate/',
            valid_rating,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(slug, response.data['slug'])

    def test_user_cant_rate_their_article(self):
        response = self.client.post(
            f'/api/articles/{slug}/rate/',
            valid_rating,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn(
            'you cant rate your own article', response.data['ratings']
            )

    def test_authenticated_user_can_rate_an_article(self):
        self.client.logout()
        signup_and_login_user(User, valid_user2, self.client)
        response = self.client.post(
            f'/api/articles/{slug}/rate/',
            valid_rating,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_one_can_only_rate_from_0_to_5(self):
        self.client.logout()
        signup_and_login_user(User, valid_user2, self.client)
        response = self.client.post(
            f'/api/articles/{slug}/rate/',
            invalid_rating,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'only digits from 0 to 5 are allowed', response.data['ratings']
            )

    def test_one_can_only_rate_from_0_to_5_other_edge_case(self):
        self.client.logout()
        signup_and_login_user(User, valid_user2, self.client)
        response = self.client.post(
            f'/api/articles/{slug}/rate/',
            invalid_rating2,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'only digits from 0 to 5 are allowed', response.data['ratings']
            )

    def test_one_cannot_rate_article_twice_with_same_rating(self):
        self.client.logout()
        signup_and_login_user(User, valid_user2, self.client)
        self.client.post(
            f'/api/articles/{slug}/rate/',
            valid_rating,
            format="json"
        )
        response = self.client.post(
            f'/api/articles/{slug}/rate/',
            valid_rating,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)
        self.assertIn(
            'You have already rated the article', response.data['message']
            )

    def test_one_cant_rate_without_using_a_proper_integer(self):
        self.client.logout()
        signup_and_login_user(User, valid_user2, self.client)
        response = self.client.post(
            f'/api/articles/{slug}/rate/',
            invalid_integer,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn(
            'only use integers', response.data['ratings']
            )

    def test_one_cannot_rate_an_article_thats_non_existent(self):
        self.client.logout()
        signup_and_login_user(User, valid_user2, self.client)
        slug="how-good"
        response = self.client.post(
            f'/api/articles/{slug}/rate/',
            valid_rating,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn(
            'Not found.', response.data['detail']
            )
