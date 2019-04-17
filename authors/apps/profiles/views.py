from rest_framework import status
from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers

from .exceptions import ProfileDoesNotExist
from .models import Profile
from .renderers import ProfileJSONRenderer
from .serializers import ProfileSerializer, RetrieveProfiles


class ProfileRetrieveAPIView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def retrieve(self, request, username, *args, **kwargs):
        try:
            # We use the `select_related` method to avoid making unnecessary
            # database calls.
            profile = Profile.objects.select_related('user').get(
                user__username=username
            )
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist

        serializer = self.serializer_class(profile, context={
            'request': request
        })

        return Response(serializer.data, status=status.HTTP_200_OK)


class RetrieveProfilesView(RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer

    def retrieve(self,request):
        profiles = Profile.objects.filter().order_by('-created_at')
        serializer = RetrieveProfiles(profiles, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
            )


class ProfileFollowAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (ProfileJSONRenderer,)
    serializer_class = ProfileSerializer        

    def delete(self, request, username=None):
        follower = self.request.user.profile

        try:
            some_one_being_followed = Profile.objects.get(
                user__username=username)
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist

        if not follower.is_following(some_one_being_followed):
            raise serializers.ValidationError(
                "You cannot unfollow a user you are not following")

        follower.unfollow(some_one_being_followed)

        serializer = self.serializer_class(
            some_one_being_followed, context={
            'request': request
        })

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, username=None):
        follower = self.request.user.profile

        try:
            some_one_being_followed = Profile.objects.get(
                user__username=username)
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist

        if follower.pk is some_one_being_followed.pk:
            raise serializers.ValidationError(
                'You cannot follow yourself')

        if follower.is_following(some_one_being_followed):
            raise serializers.ValidationError(
                'You are already following that author')

        follower.follow(some_one_being_followed)

        serializer = self.serializer_class(some_one_being_followed, context={
            'request': request
        })

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class FollowerFollowingAPIView(ListAPIView):
    """
    This API returns a list of user followers and following
    """
    serializer_class = ProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request, username, format=None):
        """Returns the user's followed user"""
        try:
            profile = Profile.objects.select_related('user').get(
                user__username=username
            )
        except Profile.DoesNotExist:
            raise ProfileDoesNotExist

        if request.user.username != username:
            raise serializers.ValidationError(
                "Only account owners can see their followers and followees"
            )

        user_follows = profile.follows.all()
        user_followed_by = profile.followed_by.all()

        follower_serializer = self.serializer_class(
            user_follows, many=True, context={
            'request': request
        })

        following_serializer = self.serializer_class(
            user_followed_by, many=True, context={
            'request': request
        })

        response = {
            "Followers":{
                "count": len(following_serializer.data),
                "data": following_serializer.data
            },
            "Following":{
                "count": len(follower_serializer.data),
                "data": follower_serializer.data
            }
        }
        return Response(response, status=status.HTTP_200_OK)
