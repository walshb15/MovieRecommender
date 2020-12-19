from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.models import User
import pandas as p
from .models import Movie
from .models import Rating
from .models import users
from .recommendDriver import movieGetter, getSimilarUsers, userBasedRecommendations, queryToList, topMoviesByGenre


'''def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn'''

def home(request):
    curUserId = 1
    #If user is logged in
    if (request.user.is_authenticated):
        '''name = str(request.user.username)
        print(name)
        if (users.objects.filter(username=name).count() > 0):
            userObj = users.objects.get(username=name)
            curUserId = userObj.userID
        elif (User.objects.filter(username=name).count() > 0):
            curUserId = request.user.id
        try:
            userObj = users.objects.get(username=name)
        except NameError:
            userObj = User.objects.get(username=name)
        print(userObj)'''
        #Get their id
        curUserId = request.user.id
        #curUserId = userObj.userID
    #If the user is not logged in, redirect to the login page
    else:
        return redirect('login')
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
    gTitles = movieGetter(genreBasedIds)

    context = {
        'uMovies':  ubTitles,
        'gMovies': gTitles,
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
        if(request.user.is_authenticated):
            name = str(request.user.username)
            #insert the rating to the database
            #What is this? Why did you use an absolute path???
            '''database = "C://Users//wolfe//Desktop//MovieRecommender//db.sqlite3"
            con = create_connection(database)
            cursor = con.cursor()'''
            
            #getUserID = "SELECT userid FROM users WHERE username = ((?))"
            getUserID = users.objects.get(name)
            #userIDLine = cursor.execute(getUserID, (name,))
            #userIDLine = cursor.fetchone()
            userIDLine = getUserID
            if userIDLine is not None:
                #userID = userIDLine[0]
                userID = getUserID.userID
                print(userID)
                '''getMovieID = "SELECT movieid FROM Movies WHERE title = ((?))"
                movieIDLine = cursor.execute(getMovieID, (movie,))
                movieIDLine = cursor.fetchone()'''
                getMovieID = Movie.objects.get(title=movie)
                movieIDLine = getMovieID
                if(movieIDLine is not None):
                    #movieID = movieIDLine[0]
                    movieID = getMovieID.movieid
                    print(movieID)
                    '''insert = "INSERT into ratings(userid, movieid, rating) VALUES((?), (?), (?))"
                    cursor.execute(insert, (userID, movieID, int(rating), ))
                    con.commit()   '''
                    insert = Rating(userid=userID, movieid=movieID, rating=int(rating))
                    insert.save()
                    messages.success(request, f'Your review has been submitted')
                    return redirect('movieRecommender-home')
                else:
                    messages.error(request, f'Your movie title was not found, please check the spelling and try again. Must match the database formatting as well.')
                    return redirect('account')
            else:
                messages.error(request, f'Please login to submit an account')
                return redirect('login')
        else:
            messages.error(request, f'Please login to submit an account')
            return redirect('login')
    else:
        return render(request, 'movieRecommender/account.html', {'title': 'Account'})
