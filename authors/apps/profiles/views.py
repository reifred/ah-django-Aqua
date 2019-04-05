from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
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

        serializer = self.serializer_class(profile)

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
