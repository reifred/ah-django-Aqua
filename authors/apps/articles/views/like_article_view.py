from django.http import Http404
from django.core import exceptions

from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView

from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)

from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Article, LikesDislikesModel
from ..renderers import ArticleJSONRenderer
from ..serializers import (
    ArticleSerializer, LikeDislikeSerializer
    )
from ..exceptions import ArticleDoesNotExist
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404


class LikeView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = LikeDislikeSerializer

    def post(self, request, slug):
        user = request.user
        article_to_be_liked = get_object_or_404(Article, slug=slug)
        check_if_article_is_liked = LikesDislikesModel.objects.filter(
            article_id = article_to_be_liked.id,
            user_liking_id = user.profile.id
        )

        if len(check_if_article_is_liked) == 0:
            serializer_data = self.serializer_class(data={
                "user_liking": user.profile.id,
                "article": article_to_be_liked.id,
                "likes": True
            })
            serializer_data.is_valid(raise_exception=True)
            serializer_data.save()
            data = {
                "article": article_to_be_liked.title,
                "username": user.username,
                "likes": serializer_data.data['likes'],
                "created_at": ((check_if_article_is_liked.first())).event_date
            }
        # we define the values that will update the records table
        check_if_article_is_liked.update(likes=True)
        likes = LikesDislikesModel.objects.filter(
            article=article_to_be_liked.id, likes=True)
        dislikes = LikesDislikesModel.objects.filter(
            article=article_to_be_liked.id, likes=False)
        # update records table
        Article.objects.filter(slug=slug).update(
            likes=(len(likes)),
            dislikes=(len(dislikes)),
        )
        data = {
                "article": article_to_be_liked.title,
                "username": user.profile.user.username,
                "likes": check_if_article_is_liked.first().likes,
                "created_at": check_if_article_is_liked.first().event_date
                }
        return Response(data, status=status.HTTP_201_CREATED)


class DislikeView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = LikeDislikeSerializer

    def post(self, request, slug):
        user = request.user
        article_to_be_liked = get_object_or_404(Article, slug=slug)
        check_if_article_is_liked = LikesDislikesModel.objects.filter(
            article_id = article_to_be_liked.id,
            user_liking_id = user.profile.id
        )

        if not check_if_article_is_liked:
            serializer_data = self.serializer_class(data={
                "user_liking": user.profile.id,
                "article": article_to_be_liked.id,
                "likes": False
            })
            serializer_data.is_valid(raise_exception=True)
            serializer_data.save()
            data = {
                "article": article_to_be_liked.title,
                "username": user.profile.user.username,
                "likes": serializer_data.data['likes'],
                "created_at": ((check_if_article_is_liked.first())).event_date
            }
        check_if_article_is_liked.update(likes=False)
        data = {
            "article": article_to_be_liked.title,
            "username": user.username,
            "likes": check_if_article_is_liked.first().likes,
            "created_at": check_if_article_is_liked.first().event_date
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
