from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Movie(models.Model):
    movieid = models.IntegerField(db_column='movieId', blank=True, null=False, primary_key=True)  # Field name made lowercase.
    title = models.TextField(blank=True, null=True)
    genre = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        managed = False
        db_table = 'movies'


class Rating(models.Model):
    ratingid = models.IntegerField(blank=True, null=False, primary_key=True)
    userid = models.IntegerField(blank=True, null=False)
    movieid = models.IntegerField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return 'Rating ID: {}'.format(self.ratingid)

    class Meta:
        managed = False
        db_table = 'ratings'

class users(models.Model):
    userID = models.IntegerField(db_column='userID', blank=True, null=True)
    username = models.TextField(blank=True, null=True)

    def __str__(self):
        return 'User ID: {}'.format(self.userID)

    class Meta:
        managed = False
        db_table = 'ratings'