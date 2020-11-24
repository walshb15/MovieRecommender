from django.contrib import admin
from .models import Post
from .models import Movie
from .models import Rating

# Register your models here.

admin.site.register(Post)
admin.site.register(Movie)
admin.site.register(Rating)