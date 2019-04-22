from django.urls import path
from .views import CommentAPIView

app_name = 'comments'
urlpatterns = [
    path('<slug:slug>/comments/', CommentAPIView.as_view()),
    path('<slug:slug>/comments/<int:pk>/', CommentAPIView.as_view())
]

