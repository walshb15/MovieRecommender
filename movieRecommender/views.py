from django.shortcuts import render
from .models import Post

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'movieRecommender/home.html', context)

def about(request):
    return render(request, 'movieRecommender/about.html', {'title': 'About'})