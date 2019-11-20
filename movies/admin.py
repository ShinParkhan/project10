from django.contrib import admin
from .models import Movie, Genre, Review
# Register your models here.


class MovieAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', 'audience',
                    'poster_url', 'description', 'genre_id')


admin.site.register(Movie, MovieAdmin)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


admin.site.register(Genre, GenreAdmin)


class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'content', 'score', 'user_id', 'movie_id')


admin.site.register(Review, ReviewAdmin)
