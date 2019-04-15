from django.conf.urls import url
from django.urls import path
from .views import ArticlesAPIView, RetrieveArticleApiView, DestroyArticleAPIView

urlpatterns = [
    path('articles/', ArticlesAPIView.as_view()),
    path('articles/<str:slug>/', RetrieveArticleApiView.as_view())
    path('articles/<slug:slug>/', DestroyArticleAPIView.as_view()),
]

