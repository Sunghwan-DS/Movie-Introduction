from django.db import models
from django.conf import settings

# Create your models here.
class Genre(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return f'{self.name}'


class RepNationNm(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return f'{self.name}'


class Movie(models.Model):
    movieNm = models.CharField(max_length=100)
    movieNmEn = models.CharField(max_length=100)
    openDt = models.DateField()
    vote_count = models.IntegerField(default=0)
    vote_tot = models.IntegerField(default=0)
    vote_average = models.FloatField(default=0)
    watchGradeNm = models.IntegerField()
    overview = models.TextField()
    repNationNm = models.ManyToManyField(RepNationNm,
                            related_name='repNationNm_movie')
    poster_path = models.CharField(max_length=100)
    backdrop_path1 = models.CharField(max_length=100)
    backdrop_path2 = models.CharField(max_length=100)
    backdrop_path3 = models.CharField(max_length=100)
    genres = models.ManyToManyField(Genre,
                            related_name='genre_movie')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                            related_name='like_movies')

    def __str__(self):
        return f'{self.movieNm}'


class Review(models.Model):
    title = models.CharField(max_length=100)
    movie = models.ForeignKey(Movie,
                             on_delete=models.CASCADE)
    rank = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    hit = models.PositiveIntegerField(default=0)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                            related_name='like_reviews')
    dislike_users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                            related_name='dislike_reviews')
    user_hit_time = models.ManyToManyField(settings.AUTH_USER_MODEL,
                            related_name='hit_time_reviews')


class Comment(models.Model):
    content = models.TextField()
    review = models.ForeignKey(Review,
                                on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                            related_name='like_comments')
    dislike_users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                            related_name='dislike_comments')


class Reply(models.Model):
    content = models.TextField()
    comment = models.ForeignKey(Comment,
                                on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                            related_name='like_reply')
    dislike_users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                            related_name='dislike_reply')


class Moviehistory(models.Model):
    movie = models.ForeignKey(Movie,
                             on_delete=models.CASCADE)

class Reviewhistory(models.Model):
    review = models.ForeignKey(Review,
                             on_delete=models.CASCADE)