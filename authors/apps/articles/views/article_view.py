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


class ListCreateArticleAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer

    def post(self, request):
        article = request.data.get('article', {})

        serializer_context = {
            "author": request.user.profile,
            'request': request
        }
        serializer = self.serializer_class(data=article, context=serializer_context)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        articles = Article.objects.filter().order_by('-created_at')

        serializer_context = {'request': request}
        serializer = self.serializer_class(
            articles,
            many=True,
            context=serializer_context
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
