from django.db import models
from authors.apps.authentication.models import User
from authors.apps.profiles.models import Profile
from django.template.defaultfilters import slugify

from authors.apps.core.utilities import get_unique_slug

class Article(models.Model):

    slug = models.SlugField(max_length=255)

    title = models.CharField(db_index=True, max_length=255)

    description = models.TextField()

    body = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    favorited = models.BooleanField(default=False)

    favorites_count = models.IntegerField(default=0)

    author = models.ForeignKey(
        Profile,
        related_name='articles',
        on_delete=models.CASCADE)

    read_time = models.TextField()

    likes = models.IntegerField(default=0)

    dislikes = models.IntegerField(default=0)

    def __str__(self):
        return self.slug

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_unique_slug(self, self.title, 'title', 'slug')
        super().save(*args, **kwargs)


class Ratings(models.Model):
    ratings = models.DecimalField(
        max_digits=5, decimal_places=0)
    ratings_by = models.ForeignKey(
        Profile,
        related_name='ratings',
        on_delete=models.CASCADE
        )
    article = models.ForeignKey(
        Article,
        related_name="all_ratings",
        on_delete=models.CASCADE
        )
    rated_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-ratings', ]


class LikesDislikesModel(models.Model):
    user_liking = models.ForeignKey(
        Profile, related_name='user_liking' , 
        on_delete=models.CASCADE
        )
    article = models.ForeignKey(
        Article, related_name='article', 
        on_delete=models.CASCADE 
        )
    likes = models.BooleanField(default=False, null=True)
    event_date = models.DateTimeField(auto_now=True)
