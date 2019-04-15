from django.conf.urls import url
from django.urls import path
from .views import CreateArticleAPIView
from .views import DestroyArticleAPIView


urlpatterns = [
    path('articles/', CreateArticleAPIView.as_view()),
    path('articles/<slug:slug>/', DestroyArticleAPIView.as_view()),
]
