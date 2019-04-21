from rest_framework import serializers

from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    bio = serializers.CharField(allow_blank=True, required=False)
    image = serializers.SerializerMethodField
    following = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ('username', 'bio', 'image', 'following')
        read_only_fields = ('username',)

    def get_image(self, obj):
        if obj.image:
            return obj.image
        return 'https://static.productionready.io/images/smiley-cyrus.jpg' 
        ###the avatar that will be displayed in case user hasnt uploaded
        #profile picture yet.

    def get_following(self, instance):
        request = self.context.get('request', None)

        if not request:
            return False

        follower = request.user.profile
        some_one_being_followed = instance
        
        return follower.is_following(some_one_being_followed)

class RetrieveProfiles(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')

    class Meta:
        model = Profile
        exclude =('id','user','follows')
        read_only_fields = ('username',)
        

