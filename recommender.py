import pandas as p
from sklearn.metrics import pairwise
import numpy as np

mov_data = p.read_csv('movies.csv', header='infer')
rating_data = p.read_csv('ratings.csv', header='infer')
rating_data.drop(['timestamp'], axis=1, inplace=True)
#Get all of the movie ids
movie_ids = rating_data['movieId'].drop_duplicates()
print("TOTAL MOVIE IDS: ", len(movie_ids))
#print(rating_data)
#Get the average rating for each user
avg_userRatings = rating_data['rating'].groupby(rating_data['userId']).mean()
#print(avg_userRatings.head())
#Get the similarity between users
grouped_users = rating_data.groupby(['userId'], as_index=False)
userOne = grouped_users.get_group(1).drop(['userId'], axis=1)
'''for i in movie_ids:
    if i not in userOne['movieId']:
        newRow = {'movieId': i, 'rating': 0}
        userOne = userOne.append(newRow, ignore_index=True)
userOne.sort_values(by=['movieId'])
print(len(userOne['movieId']))'''
userTwo = grouped_users.get_group(2).drop(['userId'], axis=1)
'''for i in movie_ids:
    if i not in userTwo['movieId']:
        newRow = {'movieId': i, 'rating': 0}
        userTwo = userTwo.append(newRow, ignore_index=True)
userTwo = userTwo.sort_values(by=['movieId'])'''
#print(235 in userTwo['movieId'])
userA = p.DataFrame()
userB = p.DataFrame()
for i in userOne.values:
    twoVal = userTwo.loc[userTwo['movieId'] == i[0]]['rating']
    if len(twoVal.values) > 0:
        userB = userB.append({'movieId': i[0], 'rating': twoVal.values[0]}, ignore_index=True)
        userA = userA.append({'movieId': i[0], 'rating': i[1]}, ignore_index=True);
print(userA)
print('\n')
print(userB)
print('\n')
#We nust now insert movies that have not been rated yet into each user's DF
#so that we can compare the similarity in ratings between each user
user_sim = p.DataFrame(pairwise.rbf_kernel([userA['rating']], [userB['rating']], gamma=0.2))
print('USER SIMILARITY SCORE:')
print(user_sim.values[0][0])
#Get the similarity between movies
