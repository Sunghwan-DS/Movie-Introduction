from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, Review, Comment, Reply, Moviehistory, Reviewhistory
from .forms import ReviewForm, CommentForm, ReplyForm, MoviehistoryForm, ReviewhistoryForm
from accounts.forms import UserhistoryForm, UservisitedreviewForm
from accounts.models import Userhistory, Uservisitedreview, User
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
import random
import time

# Create your views here.
def index(request):
    user = request.user
    # if user.is_authenticated and user.adult:
    movies = Movie.objects.all()
    # else:
    #     movies = Movie.objects.filter(adult=False)

    paginator = Paginator(movies, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    recommend_recently = Movie.objects.order_by('-openDt')[:10]
    recommend_rank = Movie.objects.order_by('-vote_average')[:10]
    # recommend_num_of_reviews = Movie.objects.order_by('-.review.count()')
    live_movie_history = Moviehistory.objects.all()
    live_movie_dict = {}
    for history in live_movie_history:
        if history.movie in live_movie_dict:
            live_movie_dict[history.movie] += 1
        else:
            live_movie_dict[history.movie] = 1
    live_movie_list = []
    for key in live_movie_dict:
        live_movie_list.append((live_movie_dict[key], key))
    live_movie_list.sort(reverse=True, key = lambda x : x[0])

    live_movies = []
    min_num = min(10, len(live_movie_list))
    for i in range(min_num):
        live_movies.append(live_movie_list[i][1])


    live_review_history = Reviewhistory.objects.all()
    live_review_dict = {}
    for history in live_review_history:
        if history.review in live_review_dict:
            live_review_dict[history.review] += 1
        else:
            live_review_dict[history.review] = 1
    live_review_list = []
    for key in live_review_dict:
        live_review_list.append((live_review_dict[key], key))
    live_review_list.sort(reverse=True, key = lambda x : x[0])

    live_reviews = []
    min_num = min(5, len(live_review_list))
    for i in range(min_num):
        live_reviews.append(live_review_list[i][1])


    users = User.objects.all()
    users_data = []
    for u in users:
        if not u.is_superuser:
            users_data.append((Review.objects.filter(user=u).count(), Comment.objects.filter(user=u).count(), u))
    users_data.sort(reverse=True, key = lambda x : (x[0], x[1]))

    best_users = []
    min_val = min(5, len(users_data))
    for i in range(min_val):
        best_users.append(users_data[i][2])


    manyReviewsList = []
    for movie in movies:
        manyReviewsList.append((movie.review_set.count(), movie))
    manyReviewsList.sort(reverse=True, key = lambda x: x[0])
    manyReviewsMovies = []

    for i in range(10):
        manyReviewsMovies.append(manyReviewsList[i][1])



    context ={
        'movies':movies,
        'page_obj': page_obj,
        'recommend_recently': recommend_recently,
        'recommend_rank': recommend_rank,
        'live_movies': live_movies,
        'live_reviews': live_reviews,
        'best_users':best_users,
        'manyReviewsMovies':manyReviewsMovies
    }
    return render(request, 'movies/index.html', context)


def movie_list(request):
    user = request.user
    # if user.is_authenticated and user.adult:
    movies = Movie.objects.order_by('-pk')
    # else:
    #     movies = Movie.objects.filter(adult=False)

    paginator = Paginator(movies, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context ={
        'movies':movies,
        'page_obj': page_obj,
    }
    return render(request, 'movies/movie_list.html', context)


def search(request):
    search = request.GET.get('search')
    movies = Movie.objects.filter(movieNm__contains=search).order_by('-pk')
    paginator = Paginator(movies, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'movies': movies,
        'page_obj': page_obj,
    }
    return render(request, 'movies/movie_list.html', context)


def rank(request):
    users_with_admin = User.objects.all()
    users = []
    for user in users_with_admin:
        if not user.is_superuser:
            users.append(user)

    movies = Movie.objects.all()

    manyLikedMoviess = []
    for movie in movies:
        manyLikedMoviess.append((movie.like_users.count(), movie))
    manyLikedMoviess.sort(reverse=True, key = lambda x : x[0])
    manyLikedMovies = []
    for movie in manyLikedMoviess[:10]:
        manyLikedMovies.append(movie[1])


    reviews = Review.objects.all()
    manyLikedReviewss = []
    for review in reviews:
        manyLikedReviewss.append((review.like_users.count(), review))
    manyLikedReviewss.sort(reverse=True, key = lambda x : x[0])
    manyLikedReviews = []
    for review in manyLikedReviewss[:10]:
        manyLikedReviews.append(review[1])


    manyHitsReviews = []
    manyHitsReviews_list = reviews.order_by('-hit')
    for review in manyHitsReviews_list[:10]:
        manyHitsReviews.append(review)

    manyCommentsReviews_list = []
    for review in reviews:
        manyCommentsReviews_list.append((review.comment_set.count(), review))
    manyCommentsReviews_list.sort(reverse=True, key = lambda x : x[0])
    manyCommentsReviews = []
    for review in manyCommentsReviews_list[:10]:
        manyCommentsReviews.append(review[1])


    live_movie_history = Moviehistory.objects.all()
    live_movie_dict = {}
    for history in live_movie_history:
        if history.movie in live_movie_dict:
            live_movie_dict[history.movie] += 1
        else:
            live_movie_dict[history.movie] = 1
    live_movie_list = []
    for key in live_movie_dict:
        live_movie_list.append((live_movie_dict[key], key))
    live_movie_list.sort(reverse=True, key = lambda x : x[0])

    live_movies = []
    min_num = min(10, len(live_movie_list))
    for i in range(min_num):
        live_movies.append(live_movie_list[i][1])


    live_review_history = Reviewhistory.objects.all()
    live_review_dict = {}
    for history in live_review_history:
        if history.review in live_review_dict:
            live_review_dict[history.review] += 1
        else:
            live_review_dict[history.review] = 1
    live_review_list = []
    for key in live_review_dict:
        live_review_list.append((live_review_dict[key], key))
    live_review_list.sort(reverse=True, key = lambda x : x[0])

    live_reviews = []
    min_num = min(10, len(live_review_list))
    for i in range(min_num):
        live_reviews.append(live_review_list[i][1])


    users_list = User.objects.all()
    users = []
    for u in users_list:
        if not u.is_superuser:
            users.append((u, Review.objects.filter(user=u).count(), Comment.objects.filter(user=u).count()))
    users.sort(reverse=True, key = lambda x : (x[1], x[2]))

    users_rank = []
    for u in users[:10]:
        users_rank.append(u[0])


    context = {
        'manyLikedMovies':manyLikedMovies,
        'manyLikedReviews':manyLikedReviews,
        'manyHitsReviews':manyHitsReviews,
        'manyCommentsReviews':manyCommentsReviews,
        'live_movies':live_movies,
        'live_reviews':live_reviews,
        'users_rank':users_rank,

    }
    return render(request, 'movies/rank.html', context)


def review_list(request):
    user = request.user
    reviews = Review.objects.order_by('-created_at')

    paginator = Paginator(reviews, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context ={
        'reviews':reviews,
        'page_obj': page_obj,
    }
    return render(request, 'movies/review_list.html', context)


def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    tot_liked = movie.like_users.all().count
    male_liked = movie.like_users.all().filter(sex='남').count()
    female_liked = movie.like_users.all().filter(sex='여').count()
    liked_50 = movie.like_users.all().filter(age__gte=49).count()
    liked_40 = movie.like_users.all().filter(age__gte=39).filter(age__lt=49).count()
    liked_30 = movie.like_users.all().filter(age__gte=29).filter(age__lt=39).count()
    liked_20 = movie.like_users.all().filter(age__gte=19).filter(age__lt=29).count()
    liked_10 = movie.like_users.all().filter(age__lt=19).count()

    recommend_movies = []
    target_genre = []

    for genre in movie.genres.all():
        target_genre.append(genre.name)

    stop = 0
    movies = Movie.objects.all()
    while len(recommend_movies) < 3 and stop < 100:
        stop += 1
        sample = random.choice(movies)
        if sample in recommend_movies:
            continue
        if sample == movie:
            continue

        for genre in sample.genres.all():
            if genre.name in target_genre:
                recommend_movies.append(sample)
                break
    # Review.objects.all()
    # male_liked = movie.like_users.all().filter(sex='남').count()

    if request.user.is_authenticated:
        if Userhistory.objects.all().filter(user=request.user).count() >= 50:
            Userhistory.objects.all().filter(user=request.user).order_by('pk')[0].delete()
        form = UserhistoryForm(request.POST)
        userhistory = form.save(commit=False)
        userhistory.user = request.user
        userhistory.movie_pk = movie_pk
        userhistory.save()


    reviews = Review.objects.order_by('-pk').filter(movie=movie)
    paginator = Paginator(reviews, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    if Moviehistory.objects.all().count() >= 1000:
        Moviehistory.objects.all().order_by('pk')[0].delete()

    form = MoviehistoryForm(request.POST)
    new_moviehistory = form.save(commit=False)
    new_moviehistory.movie = movie
    new_moviehistory.save()

    bestReviewList = []
    for review in reviews:
        bestReviewList.append((review.like_users.count(), review.dislike_users.count(), review.hit, review))
    bestReviewList.sort(reverse=True, key = lambda x: (x[0], x[2]))

    bestReviews = []
    for sample in bestReviewList:
        if sample[0]:
            if (sample[0] / (sample[0] + sample[1])) > 0.8:
                bestReviews.append(sample[3])
        if len(bestReviews) >= 3:
            break


    context = {
        'movie':movie,
        'male_liked':male_liked,
        'female_liked':female_liked,
        'liked_10':liked_10,
        'liked_20':liked_20,
        'liked_30':liked_30,
        'liked_40':liked_40,
        'liked_50':liked_50,
        'tot_liked':tot_liked,
        'recommend_movies':recommend_movies,
        'reviews':reviews,
        'page_obj': page_obj,
        'bestReviews':bestReviews,
    }
    return render(request, 'movies/movie_detail.html', context)

@login_required
def like(request, movie_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)


    if movie.like_users.filter(pk=user.pk).exists():
        movie.like_users.remove(user)
        liked = False
    else:
        movie.like_users.add(user)
        liked = True


    context = {
        'liked':liked,
        'count':movie.like_users.count(),
        'male_liked':movie.like_users.all().filter(sex='남').count(),
        'female_liked':movie.like_users.all().filter(sex='여').count(),
        'liked_10':movie.like_users.all().filter(age__lt=20).count(),
        'liked_20':movie.like_users.all().filter(age__gte=20).filter(age__lt=30).count(),
        'liked_30':movie.like_users.all().filter(age__gte=30).filter(age__lt=40).count(),
        'liked_40':movie.like_users.all().filter(age__gte=40).filter(age__lt=50).count(),
        'liked_50':movie.like_users.all().filter(age__gte=50).count(),
    }

    return JsonResponse(context)


@login_required
def review_like(request, movie_pk, review_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)

    if review.like_users.filter(pk=user.pk).exists():
        review.like_users.remove(user)
        liked = False
    else:
        review.like_users.add(user)
        liked = True
        if review.dislike_users.filter(pk=user.pk).exists():
            review.dislike_users.remove(user)

    context = {
        'liked':liked,
        'disliked':False,
        'liked_count':review.like_users.count(),
        'disliked_count':review.dislike_users.count(),
        'movie_id':movie.id,
    }

    return JsonResponse(context)


@login_required
def review_dislike(request, movie_pk, review_pk):
    user = request.user
    movie = get_object_or_404(Movie, pk=movie_pk)
    review = get_object_or_404(Review, pk=review_pk)

    if review.dislike_users.filter(pk=user.pk).exists():
        review.dislike_users.remove(user)
        disliked = False
    else:
        review.dislike_users.add(user)
        disliked = True
        if review.like_users.filter(pk=user.pk).exists():
            review.like_users.remove(user)

    context = {
        'liked':False,
        'disliked':disliked,
        'liked_count':review.like_users.count(),
        'disliked_count':review.dislike_users.count(),
        'movie_id':movie.id,
    }

    return JsonResponse(context)



@login_required
def recommend(request):

    history = Userhistory.objects.all().filter(user=request.user)
    movies = Movie.objects.all()
    if history:
        record = {}
        for one_history in history:
            history_movie = get_object_or_404(Movie, pk=one_history.movie_pk)
            for genre in history_movie.genres.all():
                if genre in record:
                    record[genre] += 1
                else:
                    record[genre] = 1

        record_list = []
        for key in record:
            record_list.append((record[key], key))

        record_list.sort(reverse=True, key = lambda x : x[0])
        favorite_genre = record_list[0][1]

        recommend_movies = []

        cnt = 0
        while len(recommend_movies) < 6 and cnt < 100:
            cnt += 1
            sample_movie = random.choice(movies)
            if sample_movie in recommend_movies:
                continue

            if favorite_genre in sample_movie.genres.all():
                recommend_movies.append(sample_movie)

    else:
        favorite_genre = None
        recommend_movies = []
        while len(recommend_movies) < 6:
            sample_movie = random.choice(movies)
            if sample_movie in recommend_movies:
                continue
            recommend_movies.append(sample_movie)

    context = {
        'favorite_genre':favorite_genre,
        'recommend_movies':recommend_movies
    }

    return render(request, 'movies/recommend.html', context)

@login_required
def review_create(request, movie_pk):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.movie = get_object_or_404(Movie, pk=movie_pk)
            movie = get_object_or_404(Movie, pk=movie_pk)
            movie.vote_count += 1
            movie.vote_tot += review.rank
            movie.vote_average = round(movie.vote_tot / movie.vote_count, 1)
            movie.save()
            form.save()
            return redirect('movies:review_detail', movie_pk, review.pk)
    else:
        form = ReviewForm()
    context = {
        'form':form
    }
    return render(request, 'movies/form.html', context)


@login_required
def review_detail(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    movie = get_object_or_404(Movie, pk=movie_pk)
    comment_form = CommentForm()
    reply_form = ReplyForm()

    # if movie.watchGradeNm == 19 and request.user.age < 19:
    #     return redirect('movies:movie_detail', movie_pk)



    if Uservisitedreview.objects.all().filter(user=request.user).filter(review=review).exists():
        uservisitedreview = Uservisitedreview.objects.all().filter(user=request.user).filter(review=review)[0]
        if time.time() - uservisitedreview.visited_time > 86400:
            uservisitedreview.visited_time = int(time.time())
            uservisitedreview.save()
            review.hit += 1
            review.save()

            if Reviewhistory.objects.all().count() >= 1000:
                Reviewhistory.objects.all().order_by('pk')[0].delete()

            form = ReviewhistoryForm(request.POST)
            new_reviewhistory = form.save(commit=False)
            new_reviewhistory.review = review
            new_reviewhistory.save()

    else:
        form = UservisitedreviewForm(request.POST)
        uservisitedreview = form.save(commit=False)
        uservisitedreview.user = request.user
        uservisitedreview.review = review
        uservisitedreview.visited_time = int(time.time())
        uservisitedreview.save()
        review.hit += 1
        review.save()

        if Reviewhistory.objects.all().count() >= 1000:
            Reviewhistory.objects.all().order_by('pk')[0].delete()

        form = ReviewhistoryForm(request.POST)
        new_reviewhistory = form.save(commit=False)
        new_reviewhistory.review = review
        new_reviewhistory.save()

    comments = Comment.objects.order_by('-pk').filter(review=review)
    paginator = Paginator(comments, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    bestCommentList = []
    for comment in comments:
        bestCommentList.append((comment.like_users.count(), comment.dislike_users.count(), review))
    bestCommentList.sort(reverse=True, key = lambda x: x[0])

    bestComments = []
    for sample in bestCommentList:
        if sample[0]:
            if (sample[0] / (sample[0] + sample[1])) > 0.8:
                bestComments.append(sample[2])
        if len(bestComments) >= 3:
            break


    context = {
        'review':review,
        'comments':comments,
        'page_obj':page_obj,
        'movie':movie,
        'movie_id':movie.id,
        'comment_form': comment_form,
        'reply_form': reply_form,
        'bestComments':bestComments,
    }
    return render(request, 'movies/review_detail.html', context)


# @require_POST
@login_required
def review_update(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    old_rank = review.rank
    if request.user == review.user or request.user.is_superuser:
        if request.method == 'POST':
            form = ReviewForm(request.POST, instance=review)
            if form.is_valid():
                review = form.save(commit=False)
                review.save()
                movie = get_object_or_404(Movie, pk=movie_pk)
                movie.vote_tot -= old_rank
                movie.vote_tot += review.rank
                if movie.vote_count:
                    movie.vote_average = round(movie.vote_tot / movie.vote_count, 1)
                else:
                    movie.vote_average = 0
                movie.save()
                return redirect('movies:review_detail', movie_pk, review_pk)
        else:
            form = ReviewForm(instance=review)
        context = {
            'form': form,
        }
        return render(request, 'movies/form.html', context)
    else:
        return redirect('movies:index')


# @require_POST
@login_required
def review_delete(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    if request.user == review.user or request.user.is_superuser:
        movie = get_object_or_404(Movie, pk=movie_pk)
        movie.vote_tot -= review.rank
        movie.vote_count -= 1
        if movie.vote_count:
            movie.vote_average = round(movie.vote_tot / movie.vote_count, 1)
        else:
            movie.vote_average = 0
        movie.save()
        review.delete()
        return redirect('movies:movie_detail', movie_pk)
    return redirect('movies:review_detail', movie_pk, review_pk)


@require_POST
@login_required
def comment_create(request, movie_pk, review_pk):
    review = get_object_or_404(Review, pk=review_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.review = review
        comment.save()
    return redirect('movies:review_detail', movie_pk, review_pk)


@require_POST
@login_required
def comment_delete(request, movie_pk, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user or request.user.is_superuser:
        if request.method == 'POST':
            comment.delete()
            return redirect('movies:review_detail', movie_pk, review_pk)

    return redirect('movies:review_detail', movie_pk, review_pk)



@require_POST
@login_required
def reply_create(request, movie_pk, review_pk, comment_pk):
    comment = get_object_or_404(Comment, pk=comment_pk)
    form = ReplyForm(request.POST)
    if form.is_valid():
        reply = form.save(commit=False)
        reply.user = request.user
        reply.comment = comment
        reply.save()
    return redirect('movies:review_detail', movie_pk, review_pk)


@require_POST
@login_required
def reply_delete(request, movie_pk, review_pk, comment_pk, reply_pk):
    reply = get_object_or_404(Reply, pk=reply_pk)
    if request.user == reply.user or request.user.is_superuser:
        if request.method == 'POST':
            reply.delete()
            return redirect('movies:review_detail', movie_pk, review_pk)

    return redirect('movies:review_detail', movie_pk, review_pk)


@login_required
def comment_like(request, comment_pk):
    user = request.user
    comment = get_object_or_404(Comment, pk=comment_pk)

    if comment.like_users.filter(pk=user.pk).exists():
        comment.like_users.remove(user)
        liked = False
    else:
        comment.like_users.add(user)
        liked = True
        if comment.dislike_users.filter(pk=user.pk).exists():
            comment.dislike_users.remove(user)

    context = {
        'commentliked':liked,
        'commentdisliked':False,
        'commentliked_count':comment.like_users.count(),
        'commentdisliked_count':comment.dislike_users.count(),
    }

    return JsonResponse(context)


@login_required
def comment_dislike(request, comment_pk):
    user = request.user
    comment = get_object_or_404(Comment, pk=comment_pk)

    if comment.dislike_users.filter(pk=user.pk).exists():
        comment.dislike_users.remove(user)
        disliked = False
    else:
        comment.dislike_users.add(user)
        disliked = True
        if comment.like_users.filter(pk=user.pk).exists():
            comment.like_users.remove(user)

    context = {
        'commentliked':False,
        'commentdisliked':disliked,
        'commentliked_count':comment.like_users.count(),
        'commentdisliked_count':comment.dislike_users.count(),
    }

    return JsonResponse(context)


@login_required
def reply_like(request, reply_pk):
    user = request.user
    reply = get_object_or_404(Reply, pk=reply_pk)

    if reply.like_users.filter(pk=user.pk).exists():
        reply.like_users.remove(user)
        liked = False
    else:
        reply.like_users.add(user)
        liked = True
        if reply.dislike_users.filter(pk=user.pk).exists():
            reply.dislike_users.remove(user)

    context = {
        'replyliked':liked,
        'replydisliked':False,
        'replyliked_count':reply.like_users.count(),
        'replydisliked_count':reply.dislike_users.count(),
    }

    return JsonResponse(context)


@login_required
def reply_dislike(request, reply_pk):
    user = request.user
    reply = get_object_or_404(Reply, pk=reply_pk)

    if reply.dislike_users.filter(pk=user.pk).exists():
        reply.dislike_users.remove(user)
        disliked = False
    else:
        reply.dislike_users.add(user)
        disliked = True
        if reply.like_users.filter(pk=user.pk).exists():
            reply.like_users.remove(user)

    context = {
        'replyliked':False,
        'replydisliked':disliked,
        'replyliked_count':reply.like_users.count(),
        'replydisliked_count':reply.dislike_users.count(),
    }

    return JsonResponse(context)