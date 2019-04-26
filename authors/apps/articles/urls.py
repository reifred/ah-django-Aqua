from django.conf.urls import url, include
from django.urls import path
from .views.article_favourite_view import ArticleFavouriteAPIView
from authors.apps.articles.views.article_view import ListCreateArticleAPIView
from authors.apps.articles.views.like_article_view import (
    LikeView, DislikeView
    )
from .views.ratings_view import  RatingView
from .views.update_article_view import (
    RetrieveUpdateAPIView, RetrieveUpdateArticleAPIView
    )

urlpatterns = [
    path('articles/', ListCreateArticleAPIView.as_view()),
    path('articles/<slug:slug>/', RetrieveUpdateArticleAPIView.as_view()),
    path('articles/', include(
        ('authors.apps.comments.urls', 'comments'), namespace='comments')),
    path(
        'articles/<slug:slug>/favourite/', 
        ArticleFavouriteAPIView.as_view()
        ),
    path('articles/<str:slug>/rate/', RatingView.as_view()),
    path('articles/<str:slug>/like/', LikeView.as_view(), name = "likes"),
    path(
        'articles/<str:slug>/dislike/', 
        DislikeView.as_view(), name = "dislikes"),
]
