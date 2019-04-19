from django.http import Http404
from django.core import exceptions
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
    )
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Article, LikesDislikesModel
from .renderers import ArticleJSONRenderer
from .serializers import ArticleSerializer, LikeDislikeSerializer
from .exceptions import ArticleDoesNotExist


class ListCreateArticleAPIView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = ArticleSerializer

    def post(self, request):
        article = request.data.get('article', {})
        user_data = {"author": request.user.profile}
        serializer = self.serializer_class(data=article, context=user_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request):
        articles = Article.objects.filter().order_by('-created_at')
        serializer = self.serializer_class(articles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
        serializer = self.serializer_class(
            article_to_update, data=new_article, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, slug):
        try:
            article = Article.objects.get(slug=slug)
        except Article.DoesNotExist:
            raise Http404
        serializer = self.serializer_class(article)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LikesDislikesView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = LikeDislikeSerializer

    def post(self, request, slug):
        user = request.user
        article_to_be_liked = get_object_or_404(Article, slug=slug)
        check_if_article_is_liked = LikesDislikesModel.objects.filter(
            article_id = article_to_be_liked.id,
            user_liking_id = user.id
        )

        # user cant applaude their own stories
        if user.id == article_to_be_liked.author.id:
            return Response(
                {
                    'likes': [
                        'you cant like your own article'
                        ]
                },
                status=status.HTTP_403_FORBIDDEN
            )
        # if not liked yet, the following code is added
        if not check_if_article_is_liked:
            serializer_data = self.serializer_class(data={
                "user_liking": user.id,
                "article": article_to_be_liked.id,
                "likes": True
            })
            serializer_data.is_valid(raise_exception=True)
            serializer_data.save()
            data = {
                "article": article_to_be_liked.title,
                "username": user.username,
                "details": serializer_data.data
            }
        elif check_if_article_is_liked:
            #if the article is liked already, the opposite 
            #is used to update the data passed to the request 
            #which is a boolean oppsite of what is in the field 
            # already
            updated_value = not((check_if_article_is_liked.first()).likes)
            check_if_article_is_liked.update(likes=updated_value)
            data = {
                "article": article_to_be_liked.title,
                "username": user.username,
                "details": {
                    "likes": check_if_article_is_liked.first().likes,
                    "created_at": check_if_article_is_liked.first().event_date
                }
            }
        # we define the values that will update the records table
        likes = LikesDislikesModel.objects.filter(
            article=article_to_be_liked.id, likes=True)
        dislikes = LikesDislikesModel.objects.filter(
            article=article_to_be_liked.id, likes=False)
        # update records table
        Article.objects.filter(slug=slug).update(
            likes=(len(likes)),
            dislikes=(len(dislikes)),
        )
        return Response(data, status=status.HTTP_201_CREATED)
