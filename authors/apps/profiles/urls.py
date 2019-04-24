from django.urls import path

from .views import (
    ProfileRetrieveAPIView, RetrieveUpdateProfilesView, 
    FollowerFollowingAPIView, ProfileFollowAPIView
)


app_name = 'profiles'
urlpatterns = [
    path('profiles/<str:username>/', ProfileRetrieveAPIView.as_view()),
    path('profiles/', RetrieveUpdateProfilesView.as_view()),
    path('profiles/<str:username>/follow/', ProfileFollowAPIView.as_view()),
    path('profiles/<str:username>/following/', FollowerFollowingAPIView.as_view())
]
