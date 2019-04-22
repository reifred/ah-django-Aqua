from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from authors.apps.articles.models import Article
from authors.apps.articles.tests.test_data import valid_article
from authors.apps.authentication.models import User
from authors.apps.authentication.tests.test_data import valid_user
from authors.apps.comments.models import Comment
from authors.apps.comments.tests.test_data import (
    comment,
    valid_request_body,
    invalid_parent_comment_id,
    non_existent_article_slug)


class CreateCommentAPIViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(**valid_user)

        valid_article.update({"author_id": self.user.id})
        self.article = Article.objects.create(**valid_article)
        self.slug = self.article.slug

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_api_can_create_a_comment_with_authenticated_user(self):
        response = self.client.post(
            f'/api/articles/{self.slug}/comments/',
            valid_request_body,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_cannot_create_a_comment_with_an_unauthenticated_user(self):
        self.client.logout()

        response = self.client.post(
            f'/api/articles/{self.slug}/comments/',
            valid_request_body,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_api_cannot_comment_with_non_existent_article(self):
        response = self.client.post(
            f'/api/articles/{non_existent_article_slug}/comments/',
            valid_request_body,
            format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn(
            "does not exist", str(
                response.data["errors"]["detail"]))

    def test_api_can_create_a_thread_on_a_comment(self):
        comment.update({
            "article": self.article,
            "author": self.user.profile
        })
        parent_comment = Comment(**comment)
        parent_comment.save()

        response = self.client.post(
            f'/api/articles/{self.slug}/comments/{parent_comment.id}/',
            valid_request_body,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_api_cannot_create_a_thread_on_non_existent_comment(self):

        response = self.client.post(
            f'/api/articles/{self.slug}/comments/{invalid_parent_comment_id}/',
            valid_request_body,
            format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("errors", response.data.keys())
