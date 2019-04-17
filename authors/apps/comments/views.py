from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from authors.apps.articles.exceptions import ArticleDoesNotExist

from authors.apps.articles.models import Article

from .serializers import CommentSerializer
from .renderers import CommentJSONRenderer


class CommentAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (CommentJSONRenderer,)
    serializer_class = CommentSerializer

    def post(self, request, *args, **kwargs):
        comment = request.data.get('comment', {})
        slug = kwargs.get('slug')
        parent = kwargs.get('pk', None)
        article = self.get_article(slug)
        data = {**comment, "parent": parent}
        context = {"author": request.user.profile, "article": article}
        serializer = self.serializer_class(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status.HTTP_201_CREATED)

    def get_article(self, slug):
        try:
            article = Article.objects.get(slug=slug)
        except BaseException:
            raise ArticleDoesNotExist
        return article
