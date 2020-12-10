from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
import pandas as p
from .models import Movie
from .models import Rating
from .recommendDriver import movieGetter, getSimilarUsers, userBasedRecommendations, queryToList, topMoviesByGenre

def home(request):
    curUserId = 1
    #The max number of movies to return
    movieCap = 6
    #The min rating needed to recommend a movie
    ratingThreshold = 3
    #Max number of similar users to display
    userCap = 6
    userRatingsIds = queryToList(Rating.objects.filter(userid=curUserId).values_list('movieid'))
    #testPrinter("According to all known laws of aviation")
    mov_data = p.DataFrame(list(Movie.objects.all().values()))
    #print(mov_data.columns.values)
    rating_data = p.DataFrame(list(Rating.objects.all().values()))
    #Group users together based on id
    grouped_users = rating_data.groupby(['userid'], as_index=False)
    #Get a dataframe of the current user's info
    curUser = grouped_users.get_group(curUserId).drop(['userid'], axis=1)
    #print(rating_data.columns.values)
    similar_users = getSimilarUsers(curUserId, curUser, grouped_users, mov_data, rating_data)
    print("Similar Users:")
    print(similar_users)
    ubRecommendIds = userBasedRecommendations(curUser, grouped_users, similar_users, movieCap, ratingThreshold)
    print("Recommended Movies (User Sim):")
    print(ubRecommendIds)
    #ubTitles = movieGetter([110.0, 223.0, 260.0, 329.0, 733.0, 919.0])
    ubTitles = movieGetter(ubRecommendIds)
    userRatingsData = movieGetter(userRatingsIds, curUserId)

    # NOLAN TESTING
    genreBasedIds = topMoviesByGenre(curUserId, mov_data, rating_data, movieCap)
    print("Recommended Movies (Genre):")
    print(genreBasedIds)


    context = {
        'uMovies':  ubTitles,
        'simUsers': similar_users.head(userCap).values,
        'ratedMovies': userRatingsData
    }
    return render(request, 'movieRecommender/home.html', context)

def about(request):
    return render(request, 'movieRecommender/about.html', {'title': 'About'})
    
def account(request):
    if request.method == 'POST':
        movie = request.POST.get('Movie_Name', None)
        rating = request.POST.get('Rating',None)
        #Movie name and Rating have been obtained, now just get the user ID, and Movie ID from databases and import the rating.
        print(movie)
        print(rating)
        
        messages.success(request, f'Your review has been submitted')
        return redirect('movieRecommender-home')
    else:
        return render(request, 'movieRecommender/account.html', {'title': 'Account'})
