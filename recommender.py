import pandas as p
from sklearn.metrics import pairwise
import numpy as np

mov_data = p.read_csv('movies.csv', header='infer')
rating_data = p.read_csv('ratings.csv', header='infer')
rating_data.drop(['timestamp'], axis=1, inplace=True)
#print(rating_data)
#Get the average rating for each user
avg_userRatings = rating_data['rating'].groupby(rating_data['userId']).mean()
#print(avg_userRatings.head())
#Get the similarity between users
grouped_users = rating_data.groupby(['userId'], as_index=False)
userOne = grouped_users.get_group(1).drop(['userId'], axis=1)
print(userOne)
userTwo = grouped_users.get_group(2).drop(['userId'], axis=1)

#We nust now insert movies that have not been rated yet into each user's DF
#so that we can compare the similarity in ratings between each user


#user_sim = p.DataFrame(pairwise.rbf_kernel(userOne.to_numpy(), userTwo.to_numpy(), gamma=0.2))
#print(user_sim)
#Get the similarity between movies
