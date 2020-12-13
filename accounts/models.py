from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from movies.models import Review
# Create your models here.


class Uservisitedreview(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    review = models.ForeignKey(Review,
                             on_delete=models.CASCADE)
    visited_time = models.IntegerField()


class Userhistory(models.Model):
    movie_pk = models.IntegerField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)


class User(AbstractUser):
    age = models.IntegerField(default=0)
    rrn = models.IntegerField(default=0)
    sex = models.CharField(max_length=10, default='남')
    followings = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='follower'
        )
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='following'
        )
    nickname = models.CharField(max_length=20)