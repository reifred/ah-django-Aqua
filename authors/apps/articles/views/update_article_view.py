from django.http import Http404
from django.core import exceptions

from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView

from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)

from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Article
from ..renderers import ArticleJSONRenderer
from ..serializers import (
    ArticleSerializer
    )
from ..exceptions import ArticleDoesNotExist
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404


class RetrieveUpdateArticleAPIView(RetrieveUpdateAPIView):
    lookup_field = 'slug'
    queryset = Article.objects.select_related('author')
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer

    def update(self, request, slug, *args, **kwargs):
        try:
            article_to_update = self.queryset.get(slug=slug)
        except Article.DoesNotExist:
            raise ArticleDoesNotExist

        if request.user != article_to_update.author.user:
            raise exceptions.PermissionDenied()
            
        new_article = request.data.get("article", {})

        serializer_context = {'request': request}

        serializer = self.serializer_class(
            article_to_update, 
            data=new_article, 
            partial=True,
            context=serializer_context
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, slug):
        serializer_context = {'request': request}
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404
        serializer = self.serializer_class(article, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)
