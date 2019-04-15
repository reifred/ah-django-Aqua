from django.conf.urls import url
from django.urls import path

from .views import (
    ListCreateArticleAPIView, RetrieveUpdateArticleAPIView
)

urlpatterns = [
    path('articles/', ListCreateArticleAPIView.as_view()),
    path('articles/<slug:slug>/', RetrieveUpdateArticleAPIView.as_view())
]

