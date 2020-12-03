import pandas as p
from sklearn.metrics import pairwise
import numpy as np

mov_data = p.read_csv('movies.csv', header='infer')
rating_data = p.read_csv('ratings.csv', header='infer')
rating_data.drop(['timestamp'], axis=1, inplace=True)
#Get all of the movie ids
movie_ids = rating_data['movieId'].drop_duplicates()
#Get all of the user ids
user_ids = rating_data['userId'].drop_duplicates()
#Get the average rating for each user
avg_userRatings = rating_data['rating'].groupby(rating_data['userId']).mean()
#Group all the users together for easier browsing later
grouped_users = rating_data.groupby(['userId'], as_index=False)
'''userOne = grouped_users.get_group(1).drop(['userId'], axis=1)
for i in movie_ids:
    if i not in userOne['movieId']:
        newRow = {'movieId': i, 'rating': 0}
        userOne = userOne.append(newRow, ignore_index=True)
userOne.sort_values(by=['movieId'])
print(len(userOne['movieId']))
userTwo = grouped_users.get_group(2).drop(['userId'], axis=1)
for i in movie_ids:
    if i not in userTwo['movieId']:
        newRow = {'movieId': i, 'rating': 0}
        userTwo = userTwo.append(newRow, ignore_index=True)
userTwo = userTwo.sort_values(by=['movieId'])
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
user_sim = pairwise.rbf_kernel([userA['rating']], [userB['rating']], gamma=0.2)[0][0]
print('USER SIMILARITY SCORE:')
print(user_sim)'''

#This will probably get passed in, but it's the user currently logged in
curUserId = 3
#Get a dataframe of the current user's info
curUser = grouped_users.get_group(curUserId).drop(['userId'], axis=1)
#Dataframe to hold the users which are most similar to the current one
similar_users = p.DataFrame()
#Go through every user id
for i in user_ids:
    #Skip if you come across the current user
    if i == curUserId:
        continue
    #Grab info of other user you are comparing against
    otherUser = grouped_users.get_group(i).drop(['userId'], axis=1)
    #Trackers figure which movies both users have in common
    curTracker = p.DataFrame()
    otherTracker = p.DataFrame()
    #Go through each of the current user's ratings
    for j in curUser.values:
        #Check if the other user has rated the same movie
        otherVal = otherUser.loc[otherUser['movieId'] == j[0]]['rating']
        if len(otherVal.values) > 0:
            #If yes append the rating of each user to their respective tracker
            curTracker = curTracker.append({'movieId': j[0], 'rating': j[1]}, ignore_index=True)
            otherTracker = otherTracker.append({'movieId': j[0], 'rating': otherVal.values[0]}, ignore_index=True)
    #If the size of the trackers is zero, the two users are nothing alike
    if (otherTracker.size < 1):
        similar_users = similar_users.append({'userId': i, 'simScore': 0.0}, ignore_index=True)
        continue
    #Otherwise, calaculate the similarity score between the users and store it
    user_sim = pairwise.rbf_kernel([curTracker['rating']], [otherTracker['rating']], gamma=0.2)[0][0]
    similar_users = similar_users.append({'userId': i, 'simScore': user_sim}, ignore_index=True)
print("TOP 5 Most Similar Users to UserId", curUserId)
print(similar_users.sort_values(by='simScore', ascending=False).head())
    

