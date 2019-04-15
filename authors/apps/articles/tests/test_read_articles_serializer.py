from django.test import TestCase
from rest_framework.utils.serializer_helpers import ReturnList

from authors.apps.articles.models import Article
from authors.apps.articles.serializers import ReadArticlesSerializer
from authors.apps.articles.tests.test_data import valid_article
from authors.apps.authentication.models import User
from authors.apps.authentication.tests.test_data import valid_user


class ReadArticlesSerializerTestCase(TestCase):

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

        # initialize the serializer
        self.serializer_class = ReadArticlesSerializer

    def test_serializer_can_read_articles(self):
        articles = Article.objects.all()
        self.serializer = self.serializer_class(articles, many=True)

        self.assertIsInstance(self.serializer.data, ReturnList)
