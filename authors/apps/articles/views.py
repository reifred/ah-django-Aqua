from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework import permissions

from .renderers import ArticleJSONRenderer
from .serializers import CreateArticleSerializer
from .serializers import ArticleSerializer
from .permissions import IsOwnerOrReadOnly
from .models import Article


class CreateArticleAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = CreateArticleSerializer

    def post(self, request):
        article = request.data.get('article', {})
        article.update({"author_id": request.user.id})

        serializer = self.serializer_class(data=article)
        serializer.is_valid(raise_exception=True)
        saved_article = serializer.save()
        serializer.validated_data.update({"article": saved_article})

        return Response(
            serializer.validated_data,
            status=status.HTTP_201_CREATED)


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
