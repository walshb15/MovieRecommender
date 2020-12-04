from .models import Movie
from .models import Rating

def movieGetter(ids):
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
        #movDict["rating"] = Rating.objects.get(movieid=i).rating
        movDict["rating"] = -1
        moviesList.append(movDict)
    return moviesList