from django.urls import path

from .views import (
    ProfileRetrieveAPIView, RetrieveProfilesView, 
    FollowerFollowingAPIView, ProfileFollowAPIView
)


app_name = 'profiles'
urlpatterns = [
    path('profiles/<str:username>/', ProfileRetrieveAPIView.as_view()),
    path('profiles/', RetrieveProfilesView.as_view()),
    path('profiles/<str:username>/follow/', ProfileFollowAPIView.as_view()),
    path('profiles/<str:username>/following/', FollowerFollowingAPIView.as_view())
]
