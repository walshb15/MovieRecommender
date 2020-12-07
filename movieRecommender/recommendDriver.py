import pandas as p
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
