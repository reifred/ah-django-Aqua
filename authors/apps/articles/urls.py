from django.conf.urls import url
from django.urls import path

from .views import (
    ListCreateArticleAPIView, RetrieveUpdateDestroyAPIView
)

urlpatterns = [
    path('articles/', ListCreateArticleAPIView.as_view()),
    path('articles/<slug:slug>/', RetrieveUpdateDestroyAPIView.as_view())
]

