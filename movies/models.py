from django.db import models
from django.conf import settings
# Create your models here.


class Genre(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Movie(models.Model):
    title = models.CharField(max_length=30)
    audience = models.IntegerField()
    poster_url = models.CharField(max_length=140)
    description = models.TextField()
    like_users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='like_movies', blank=True)
    genres = models.ManyToManyField(Genre, related_name='movies')

    def __str__(self):
        return self.title


class Review(models.Model):
    content = models.CharField(max_length=140)
    score = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)

    def __str__(self):
        return self.content
