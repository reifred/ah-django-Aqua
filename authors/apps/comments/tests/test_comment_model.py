from django.test import TestCase

from authors.apps.articles.models import Article
from authors.apps.articles.tests.test_data import valid_article
from authors.apps.authentication.models import User
from authors.apps.authentication.tests.test_data import valid_user
from authors.apps.comments.models import Comment
from authors.apps.comments.tests.test_data import comment


class CommentTestCase(TestCase):
    """ This class defines the test suite for the Comment model"""

    def setUp(self):
        user = User.objects.create_user(**valid_user)
        valid_article.update({"author_id": user.id})
        article = Article.objects.create(**valid_article)

        comment.update({
            "article": article,
            "author": user.profile
        })
        self.comment = Comment(**comment)

    def test_model_can_create_a_comment(self):
        previous_count = Comment.objects.count()
        self.comment.save()
        current_count = Comment.objects.count()

        self.assertNotEqual(previous_count, current_count)
        self.assertEqual(str(self.comment), comment['body'])
