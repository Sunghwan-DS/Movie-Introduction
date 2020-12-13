from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('rank/', views.rank, name='rank'),
    path('movie_list/', views.movie_list, name="movie_list"),
    path('movie_list/search/', views.search, name='search'),
    path('review_list/', views.review_list, name="review_list"),
    path('<int:movie_pk>/', views.movie_detail, name='movie_detail'),
    path('<int:movie_pk>/like/', views.like, name='like'),
    path('recommend/', views.recommend, name='recommend'),
    path('<int:movie_pk>/create/', views.review_create, name = 'review_create'),
    path('<int:movie_pk>/<int:review_pk>/', views.review_detail, name='review_detail'),
    path('<int:movie_pk>/<int:review_pk>/like/', views.review_like, name='review_like'),
    path('<int:movie_pk>/<int:review_pk>/dislike/', views.review_dislike, name='review_dislike'),
    path('<int:movie_pk>/<int:review_pk>/update/', views.review_update, name='review_update'),
    path('<int:movie_pk>/<int:review_pk>/delete/', views.review_delete, name='review_delete'),
    path('<int:movie_pk>/<int:review_pk>/comment_create/', views.comment_create, name='comment_create'),
    path('comment/<int:comment_pk>/like/', views.comment_like, name='comment_like'),
    path('comment/<int:comment_pk>/dislike/', views.comment_dislike, name='comment_dislike'),
    path('<int:movie_pk>/<int:review_pk>/comment/<int:comment_pk>/delete', views.comment_delete, name='comment_delete'),
    path('<int:movie_pk>/<int:review_pk>/<int:comment_pk>/reply_create/', views.reply_create, name='reply_create'),
    path('<int:movie_pk>/<int:review_pk>/<int:comment_pk>/<int:reply_pk>/reply_delete/', views.reply_delete, name='reply_delete'),
    path('reply/<int:reply_pk>/like/', views.reply_like, name='reply_like'),
    path('reply/<int:reply_pk>/dislike/', views.reply_dislike, name='reply_dislike'),
]