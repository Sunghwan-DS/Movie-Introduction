from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.forms import AuthenticationForm
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.contrib.auth.decorators import login_required
from movies.models import Review, Movie, Comment
from .models import Userhistory
User = get_user_model()

# Create your views here.
def signup(request):
    flag = False
    nick_flag = False
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            check_num = 0
            for idx, mul_num in enumerate((5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2)):
                check_num += user.rrn // (10 ** (idx + 1)) % 10 * mul_num
            check_num = 11 - (check_num % 11)
            nicknames = [i.nickname for i in User.objects.all()]
            if user.nickname not in nicknames:
                if check_num == user.rrn % 10:
                    if 20 - user.rrn // 100000000000 > 0:
                        user.age = 20 - user.rrn // 100000000000
                    else:
                        user.age = 120 - user.rrn // 100000000000

                    if user.rrn // 1000000 % 10 in (2, 4):
                        user.sex = '여'
                    user.save()
                    auth_login(request, user)
                    return redirect('movies:index')

                else:
                    flag = True
            else:
                nick_flag = True

    else:
        form = CustomUserCreationForm()

    context = {
        'form':form,
        'flag':flag,
        'nick_flag':nick_flag,
    }
    return render(request, 'accounts/form.html', context)

def login(request):
    flag = False
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect(request.GET.get('next') or 'movies:index')
    else:
        form = AuthenticationForm()
    context = {
        'form':form,
        'flag':flag
    }
    return render(request,'accounts/form.html', context)

@login_required
def logout(request):
    auth_logout(request)
    return redirect('movies:index')

@login_required
def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk)
    users_list = User.objects.all()
    users = []
    for u in users_list:
        if not u.is_superuser:
            users.append((u, Review.objects.filter(user=u).count(), Comment.objects.filter(user=u).count()))
    users.sort(reverse=True, key = lambda x : (x[1], x[2]))

    for idx, u in enumerate(users):
        if u[0] == user:
            rank = idx + 1
            break
    else:
        rank = '운영자'

    if rank == '운영자':
        tier = 'gold'
    else:
        if rank <= len(users) * 0.1:
            tier = 'gold'
        elif rank <= len(users) * 0.3:
            tier = 'silver'
        else:
            tier = 'bronze'
        rank = str(rank) + '등'

    plus_age = user.age + 1
    reviews = Review.objects.filter(user_id=pk)
    comments = Comment.objects.filter(user_id=pk)

    history = Userhistory.objects.all().filter(user=user)
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
    else:
        favorite_genre = None

    context = {
        'user':user,
        'reviews':reviews,
        'comments':comments,
        'favorite_genre':favorite_genre,
        'plus_age':plus_age,
        'tier':tier,
        'rank':rank,
    }
    return render(request, 'accounts/user_detail.html', context)


def user_update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('movies:index')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {
        'form': form
    }
    return render(request, 'accounts/update.html', context)


@login_required
def follow(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user != request.user:
        if user.followers.filter(pk=request.user.pk).exists():
            user.followers.remove(request.user)
            request.user.followings.remove(user)

        else:
            user.followers.add(request.user)
            request.user.followings.add(user)
    return redirect('accounts:detail', user.pk)

@login_required
def delete(request):
    reviews = request.user.review_set.all()
    for review in reviews:
        movie = review.movie
        movie.vote_tot -= review.rank
        movie.vote_count -= 1
        if movie.vote_count:
            movie.vote_average = round(movie.vote_tot / movie.vote_count, 1)
        else:
            movie.vote_average = 0
        movie.save()
    request.user.delete()
    return redirect('movies:index')
