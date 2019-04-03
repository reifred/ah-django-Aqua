from django.conf.urls import url
from django.urls import path
from .views import (
    LoginAPIView, RegistrationAPIView,
    UserRetrieveUpdateAPIView, ActivateAccount,
    ResetPasswordView, NewPasswordView
)

urlpatterns = [
    path('user/', UserRetrieveUpdateAPIView.as_view(), name='user-action'),
    path('users/', RegistrationAPIView.as_view(), name='register'),
    path('users/login/', LoginAPIView.as_view(), name='login'),
    path(
        'users/verify/',
        ActivateAccount.as_view(), name='activate-account'),
    path(
        'users/reset-password/', 
        ResetPasswordView.as_view(), name='reset-password'),
    path(
        'users/new-password/', 
        NewPasswordView.as_view(), name='new-password'),
]
