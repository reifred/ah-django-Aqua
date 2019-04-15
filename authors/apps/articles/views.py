from django.http import Http404
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions

from .models import Article
from .renderers import ArticleJSONRenderer
from .permissions import IsOwnerOrReadOnly
from .serializers import CreateArticleSerializer, ReadArticlesSerializer


class ArticlesAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ArticleJSONRenderer,)

    def post(self, request):
        article = request.data.get('article', {})
        article.update({"author_id": request.user.id})

        serializer = CreateArticleSerializer(data=article)
        serializer.is_valid(raise_exception=True)
        saved_article = serializer.save()
        serializer.validated_data.update({"article": saved_article})

        return Response(
            serializer.validated_data,
            status=status.HTTP_201_CREATED)

    def get(self, request):
        articles = Article.objects.filter().order_by('-created_at')
        serializer = ReadArticlesSerializer(articles, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK)


class RetrieveArticleApiView(RetrieveAPIView):
    permission_classes = (AllowAny,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ReadArticlesSerializer

    def retrieve(self, request, slug):
        article = self.get_object(slug)
        serializer = self.serializer_class(article)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK)

    def get_object(self, slug):
        try:
            return Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404

            
class DestroyArticleAPIView(APIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)

    def delete(self, request, slug, format=None):

        try:
            article = Article.objects.get(slug=slug)
            self.check_object_permissions(self.request, article)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        if request.method == 'DELETE':
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)