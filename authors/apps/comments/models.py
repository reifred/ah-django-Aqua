from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from authors.apps.profiles.models import Profile

from authors.apps.articles.models import Article


class Comment(MPTTModel):

    body = models.TextField()

    article = models.ForeignKey(
        Article,
        related_name='comments',
        on_delete=models.CASCADE)

    author = models.ForeignKey(
        Profile,
        related_name='comments',
        on_delete=models.CASCADE)
    # The parent field makes use of the mptt tree structure when
    # storing data. As such the TreeForeignkey enables creating 
    # the relationship in the database between the parent and its
    # children.
    parent = TreeForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        db_index=True,
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class MPTTMeta:
        order_insertion_by = ['created_at']

    def __str__(self):
        return self.body
