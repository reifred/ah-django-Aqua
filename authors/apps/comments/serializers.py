from rest_framework import serializers

from authors.apps.articles.models import Article
from authors.apps.profiles.serializers import ProfileSerializer

from .models import Comment


class RecursiveField(serializers.Serializer):
    def to_representation(self, instance):
        serializer = self.parent.parent.__class__(
            instance,
            context=self.context
        )
        return serializer.data


class CommentSerializer(serializers.ModelSerializer):
    # Assign this serializer to all child fields(threads) in the
    # comment tree using the RecursiveField class
    children = RecursiveField(required=False, many=True)
    parent = serializers.SerializerMethodField
    author = ProfileSerializer(read_only=True)
    article = serializers.StringRelatedField(many=False)

    class Meta:
        model = Comment
        fields = (
            'id',
            'body',
            'article',
            'parent',
            'created_at',
            'updated_at',
            'author',
            'children',
        )

    def create(self, validated_data):
        author = self.context.get("author")
        article = self.context.get("article")
        validated_data.update({"author": author, "article": article})
        comment = Comment.objects.create(**validated_data)
        return comment
