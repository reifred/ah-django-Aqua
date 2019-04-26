from django.http import Http404
from django.core import exceptions

from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView

from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly, IsAuthenticated
)

from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Article, Ratings
from ..renderers import ArticleJSONRenderer
from ..serializers import (
    ArticleSerializer, RatingSerializer
    )
from ..exceptions import ArticleDoesNotExist
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404


class RatingView(APIView):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    renderer_classes = (ArticleJSONRenderer,)
    serializer_class = RatingSerializer

    def post(self, request, slug):
        user = request.user
        rating_field = request.data.get('article',{})
        ratings = rating_field.get('ratings',None)
        article_to_be_rated = get_object_or_404(Article, slug=slug)
        if ratings < 0 or ratings > 5:
            return Response(
                {
                    'ratings': [
                        'only digits from 0 to 5 are allowed'
                        ]
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        if not isinstance(ratings, int):
            return Response(
                {
                    'ratings': [
                        'only use integers'
                        ]
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = RatingSerializer(data=rating_field)
        serializer.is_valid(raise_exception=True)
        if user.id == article_to_be_rated.author.user_id:
            return Response(
                {
                    'ratings': [
                        'you cant rate your own article'
                        ]
                },
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            Ratings.objects.get(
                ratings_by=user.pk,
                article_id=article_to_be_rated.pk,
                ratings=ratings
            )
            return Response(
                {"message": "You have already rated the article"},
                status=status.HTTP_409_CONFLICT)
        except Ratings.DoesNotExist:
            serializer.save(
                ratings_by_id=user.pk, article=article_to_be_rated
                )
            article_id = article_to_be_rated.pk

            average_rating = Ratings.objects.filter(
                article=article_id).values(
                    'ratings').aggregate(Avg('ratings'))

            article_to_be_rated.article_rating = average_rating
            Article.article_rating = average_rating
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, slug):
        # Fetch a rated article
        article_to_be_rated = get_object_or_404(Article, slug=slug)
        average_ratings = Ratings.objects.filter(
            article=article_to_be_rated.id).values(
                'ratings').aggregate(Avg('ratings'))
        response = {
            "slug": article_to_be_rated.slug,
            "body": article_to_be_rated.body,
            "average_rating": average_ratings['ratings__avg']
        }
        return Response(response, status=status.HTTP_200_OK)
