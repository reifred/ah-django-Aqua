from django.urls import path

from .views import ProfileRetrieveAPIView, RetrieveProfilesView


app_name = 'profiles'
urlpatterns = [
    path('profiles/<str:username>/', ProfileRetrieveAPIView.as_view()),
    path('profiles/', RetrieveProfilesView.as_view()),
]
