from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    #On delete tells it to delete the post if its author is deleted
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

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
    userid = models.IntegerField(blank=True, null=False, primary_key=True)
    movieid = models.IntegerField(blank=True, null=True)
    rating = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return '{} {} {}'.format(self.userid, self.movieid, self.rating)

    class Meta:
        managed = False
        db_table = 'ratings'