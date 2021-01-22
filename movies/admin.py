from django.contrib import admin
from .models import Movie, MovieReview, Genre

admin.site.register(Movie)
admin.site.register(MovieReview)
admin.site.register(Genre)
