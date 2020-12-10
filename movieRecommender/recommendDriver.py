import pandas as p
import operator
from sklearn.metrics import pairwise
from .models import Movie
from .models import Rating

def queryToList(query):
    values = []
    for i in query:
        values.append(i[0])
    return values

def movieGetter(ids, curUserId=None):
    '''
    ids: A list of ids

    This function takes a list of ids and returns a list of movie data for each id
    '''
    moviesList = []
    for i in ids:
        movDict = dict()
        movie = Movie.objects.get(movieid=i)
        movDict["id"] = i
        movDict["title"] = movie.title
        movDict["genre"] = movie.genre
        if curUserId is not None:
            checker = Rating.objects.filter(movieid=i, userid=curUserId)
            if checker.count() > 0:
                movDict["rating"] = Rating.objects.get(movieid=i, userid=curUserId).rating
        #movDict["rating"] = -1
        moviesList.append(movDict)
    return moviesList

def getSimilarUsers(curUserId, curUser, grouped_users, mov_data, rating_data):
    #rating_data.drop(['timestamp'], axis=1, inplace=True)
    #Get all of the movie ids
    movie_ids = rating_data['movieid'].drop_duplicates()
    #Get all of the user ids
    user_ids = rating_data['userid'].drop_duplicates()
    #Get the average rating for each user
    avg_userRatings = rating_data['rating'].groupby(rating_data['userid']).mean()
    #Dataframe to hold the users which are most similar to the current one
    similar_users = p.DataFrame()
    '''
    MAKE SURE YOU GET RID OF THE .head() WHEN YOU AREN'T TESTING
    '''
    for i in user_ids.head():
        #Skip if you come across the current user
        if i == curUserId:
            continue
        #Grab info of other user you are comparing against
        otherUser = grouped_users.get_group(i).drop(['userid', 'ratingid'], axis=1)
        #Trackers figure which movies both users have in common
        curTracker = p.DataFrame()
        otherTracker = p.DataFrame()
        #Go through each of the current user's ratings
        for j in curUser.values:
            #print(j)
            #Check if the other user has rated the same movie
            otherVal = otherUser.loc[otherUser['movieid'] == j[1]]['rating']
            if len(otherVal.values) > 0:
                #print(otherVal.values)
                #If yes append the rating of each user to their respective tracker
                curTracker = curTracker.append({'movieid': j[1], 'rating': j[2]}, ignore_index=True)
                otherTracker = otherTracker.append({'movieid': j[1], 'rating': otherVal.values[0]}, ignore_index=True)
        #If the size of the trackers is zero, the two users are nothing alike
        if (otherTracker.size < 1):
            similar_users = similar_users.append({'userid': i, 'simScore': 0.0}, ignore_index=True)
            continue
        #Otherwise, calaculate the similarity score between the users and store it
        user_sim = pairwise.rbf_kernel([curTracker['rating']], [otherTracker['rating']], gamma=0.2)[0][0]
        similar_users = similar_users.append({'userid': i, 'simScore': user_sim}, ignore_index=True)
    #print("TOP 5 Most Similar Users to UserID", curUserId)
    similar_users = similar_users.sort_values(by='simScore', ascending=False)
    #print(similar_users)
    #print('\n')
    return similar_users

def userBasedRecommendations(curUser, grouped_users, similar_users, movieCap, ratingThreshold):
    #Set (used to prevent duplicates) used to hold recommended movies
    uMovieRecommendations = set()
    #Loop through the user ids of similar users
    '''
    MAKE SURE YOU GET RID OF THE .head() WHEN YOU AREN'T TESTING!
    '''
    for i in similar_users['userid'].head():
        simUser = grouped_users.get_group(i)
        #Go through the ratings from the similar user
        for j in simUser.values:
            #Find a movie that the current user has not watched yet
            existsCheck = curUser.loc[curUser['movieid'] == j[2]]
            if len(existsCheck.values) == 0:
                #If the movie that was found is above the rating threshold
                if j[3] >= ratingThreshold:
                    #Recommend it (add the ID to the list)
                    #uMovieRecommendations.append(j[1])
                    uMovieRecommendations.add(j[2])
            #Stop looping when enough movies are found
            if len(uMovieRecommendations) >= movieCap:
                break
        if len(uMovieRecommendations) >= movieCap:
            break

    #print("Top {} movies (ids) based on what similar users like:".format(movieCap))
    #print(uMovieRecommendations)
    return uMovieRecommendations


'''
@descrip: Gets list of new movies based on user's most watched genres

@param userId: The user receiving recommendations
@param movieData: Data from teh Movies table
@param ratingData: Data from the Ratings table
@param movieCap: The max movies to get
@return: A dictionary of form {Genre : [movieIds]}
'''
def newMoviesByGenre(userId, movieData, ratingData, movieCap):
    genreCounts = dict()
    total = 0

    userMovies = ratingData.loc[ratingData['userid'] == userId]['movieid'].to_list()

    # Get the number of movies the user has seen for each genre
    for movie in movieGetter(userMovies):
        for genre in movie['genre'].split('|'): 
            if genreCounts.get(genre, False):
                genreCounts[genre] += 1
            else:
                genreCounts[genre] = 1
            total += 1

    # Adjust counts to be a proportion of the movie cap
    for k in genreCounts.keys():
        genreCounts[k] = round((genreCounts[k]/total) * movieCap)

    movies = set()
    # Get movies the user hasnt seen for each genre
    for genre in genreCounts:
        movieid = movieData[movieData['genre'].str.contains(genre)]['movieid'].to_list()
        step = 0
        while genreCounts[genre] > 0:
            try:
                if movieid[step] not in movies and movieid[step] not in userMovies:
                    genreCounts[genre] -= 1
                    movies.add(movieid[step])
                step += 1
            except: 
                break


    return movies 

    
'''
@descrip: Gets movies recommendations for user based on top genres

@param userId: The ID of the user being recommeded to
@param movieData: Data from teh Movies table
@param ratingData: Data from the Ratings tableparam movieData
@param movieCap: The max number of movies to get

@return: Set of movies IDs with highest recommendations
'''
def topMoviesByGenre(userId, movieData, ratingData, movieCap):
    movies = newMoviesByGenre(userId, movieData, ratingData, movieCap * 100)
    userRatings = list(zip(ratingData.loc[ratingData['userid'] == userId]['movieid'].to_list(), ratingData.loc[ratingData['userid'] == userId]['rating'].to_list()))

    genreAvgs = dict()  # {Genre : (avgRating, totalRatings)}

    # Get ratings by genre
    for rating in userRatings:
        for genre in str(movieData.loc[movieData['movieid'] == rating[0]]['genre']).split()[1].split('|'):
            if genreAvgs.get(genre, False):
                genreAvgs[genre] = (genreAvgs[genre][0] + rating[1], genreAvgs[genre][1] + 1)
            else:
                genreAvgs[genre] = (rating[1], 1)

    recommendedRatings = list() # [MovieId, RecommendationRating]

    # Recommend movies based on weighted average rating by genre
    for movieId in movies:
        rating = 0
        for genre in str(movieData.loc[movieData['movieid'] == movieId]['genre']).split()[1].split('|'):
            if genreAvgs.get(genre, False):
                rating += genreAvgs[genre][0] / genreAvgs[genre][1]
        recommendedRatings.append((movieId, rating))

    recommendedRatings.sort(key = operator.itemgetter(1), reverse=True)
    return set(list(zip(*recommendedRatings[:movieCap]))[0])

     