from django.shortcuts import render
import pandas as p
from .models import Movie
from .models import Rating
from .recommendDriver import movieGetter, getSimilarUsers, userBasedRecommendations, queryToList

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
    print("Recommended Movies:")
    print(ubRecommendIds)
    #ubTitles = movieGetter([110.0, 223.0, 260.0, 329.0, 733.0, 919.0])
    ubTitles = movieGetter(ubRecommendIds)
    userRatingsData = movieGetter(userRatingsIds, curUserId)
    context = {
        'uMovies':  ubTitles,
        'simUsers': similar_users.head(userCap).values,
        'ratedMovies': userRatingsData
    }
    return render(request, 'movieRecommender/home.html', context)

def about(request):
    return render(request, 'movieRecommender/about.html', {'title': 'About'})