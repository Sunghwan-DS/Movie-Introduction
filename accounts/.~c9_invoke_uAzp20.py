from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    adult = models.BooleanField(default = False)
    rrn = models.IntegerField()
    followers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='followings'
        )

    Adventure = models.IntegerField(default = 0)
    Fantasy = models.IntegerField(default = 0)
    Animation = models.IntegerField(default = 0)
    Drama = models.IntegerField(default = 0)
    Horror = models.IntegerField(default = 0)
    Action = models.IntegerField(default = 0)
    Comedy = models.IntegerField(default = 0)
    History = models.IntegerField(default = 0)
    Western = models.IntegerField(default = 0)
    Thriller = models.IntegerField(default = 0)
    Crime = models.IntegerField(default = 0)
    Documentary = models.IntegerField(default = 0)
    ScienceFiction = models.IntegerField(default = 0)
    Mystery = models.IntegerField(default = 0)
    Music = models.IntegerField(default = 0)
    Romance = models.IntegerField(default = 0)
    Family = models.IntegerField(default = 0)
    War = models.IntegerField(default = 0)
    TVMovie = models.IntegerField(default = 0)

