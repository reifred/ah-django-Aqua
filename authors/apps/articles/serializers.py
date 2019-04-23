from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers

from authors.apps.authentication.serializers import UserSerializer
from authors.apps.profiles.serializers import ProfileSerializer

from authors.apps.authentication.serializers import UserSerializer
from .models import Article

import readtime

from authors.apps.core.utilities import get_unique_slug


class ArticleSerializer(serializers.ModelSerializer):
    """Serializes create article requests and creates an article"""
    title = serializers.CharField(max_length=255, min_length=2)
    slug = serializers.SlugField(required=False)
    description = serializers.CharField()
    body = serializers.CharField()
    author = ProfileSerializer(read_only=True)
    createdAt = serializers.SerializerMethodField(method_name='get_created_at')
    updatedAt = serializers.SerializerMethodField(method_name='get_updated_at')
    favoritesCount = serializers.SerializerMethodField(method_name='get_favorites_count')
    read_time = serializers.SerializerMethodField(method_name='get_readTime')
    favourited = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'slug', 'title', 'description', 'body', 'createdAt', 
            'updatedAt', 'read_time', 'favourited', 'favoritesCount', 'author']

    def get_created_at(self, obj):
        return obj.created_at
    
    def get_updated_at(self, obj):
        return obj.updated_at

    def get_favorites_count(self, instance):
        return instance.favourited_by.count()

    def get_readTime(self, obj):
        read_time = f"{str(readtime.of_text(obj.body, wpm =256).text)} read"
        return read_time

    def get_favourited(self, instance):
        request = self.context.get('request', None)

        if not request:
            return False

        if not request.user.is_authenticated:
            return False

        return request.user.profile.is_favourited(instance)

    def create(self, validated_data):
        author = self.context.get("author", None)
        return Article.objects.create(author=author, **validated_data)
    
    def update(self, instance, validated_data):
        article_object = Article()

        if "title" in validated_data.keys():
            title = validated_data.get('title')
            instance.slug = get_unique_slug(article_object, title, 'title', 'slug')
        
        for (key, value) in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance
