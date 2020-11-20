from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='movieRecommender-home'),
    path('about/', views.about, name='movieRecommender-about'),
]