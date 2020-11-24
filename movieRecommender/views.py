from django.shortcuts import render
from .models import Movie
from .models import Rating

def home(request):
    context = {
        'movies': Movie.objects.all()
    }
    return render(request, 'movieRecommender/home.html', context)

def about(request):
    return render(request, 'movieRecommender/about.html', {'title': 'About'})