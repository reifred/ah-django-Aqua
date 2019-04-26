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


class ArticleFavouriteAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer

    def post(self, request, slug):
        profile = request.user.profile
        serializer_context = {'request': request}

        article = self.get_article(slug)

        profile.favourite(article)

        serializer = self.serializer_class(article, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, slug):
        profile = request.user.profile
        serializer_context = {'request': request}

        article = self.get_article(slug)

        profile.unfavourite(article)

        serializer = self.serializer_class(article, context=serializer_context)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def get_article(self, slug):
        try:
            return Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404
