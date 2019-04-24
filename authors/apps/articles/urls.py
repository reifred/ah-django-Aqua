from django.conf.urls import url, include
from django.urls import path

from .views import (
    ListCreateArticleAPIView, RetrieveUpdateArticleAPIView, 
    ArticleFavouriteAPIView,
    RatingView
)

urlpatterns = [
    path('articles/', ListCreateArticleAPIView.as_view()),
    path('articles/<slug:slug>/', RetrieveUpdateArticleAPIView.as_view()),
    path('articles/', include(('authors.apps.comments.urls', 'comments'), namespace='comments')),
    path('articles/<slug:slug>/favourite/', ArticleFavouriteAPIView.as_view()),
    path('articles/<str:slug>/rate/', RatingView.as_view()),
]

