from django.shortcuts import render
from .models import Movie
from .models import Rating
from .recommendDriver import movieGetter

def home(request):
    testPrinter("According to all known laws of aviation")
    testTitles = movieGetter([110.0, 223.0, 260.0, 329.0, 733.0, 919.0])
    context = {
        'uMovies':  testTitles
    }
    return render(request, 'movieRecommender/home.html', context)

def about(request):
    return render(request, 'movieRecommender/about.html', {'title': 'About'})