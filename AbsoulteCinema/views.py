from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Movie, Review, Favourite, WatchHistory, Rating
from .forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile


def index(request):
    return render(request, 'index.html')


def home(request):
    movies = Movie.objects.all()[:5]
    return render(request, 'home.html', {'movies': movies})


def movies(request):
    movies = Movie.objects.all()
    return render(request, 'movies.html', {'movies': movies})


def movie_detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = movie.reviews.all()
    ratings = movie.ratings.all()
    return render(request, 'movieDetails.html', {
        'movie': movie,
        'reviews': reviews,
        'ratings': ratings
    })


def ranked(request):
    movies = Movie.objects.annotate(avg_rating=Avg('ratings__score')).order_by('-avg_rating')
    return render(request, 'movies.html', {'movies': movies})


@login_required
def add_rating(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        score = request.POST.get('score')
        if score:
            Rating.objects.update_or_create(
                user=request.user,
                movie=movie,
                defaults={'score': score}
            )

    return redirect('AbsoluteCinema:movie_detail', movie_id=movie.id)


@login_required
def add_review(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Review.objects.create(
                user=request.user,
                movie=movie,
                content=content
            )

    return redirect('AbsoluteCinema:movie_detail', movie_id=movie.id)


@login_required
def profile(request):
    favourites = Favourite.objects.filter(user=request.user)
    watch_history = WatchHistory.objects.filter(user=request.user)
    reviews = Review.objects.filter(user=request.user)
    return render(request, 'profile.html', {
        'favourites': favourites,
        'watch_history': watch_history,
        'reviews': reviews
    })


@login_required
def favourites(request):
    favourites = Favourite.objects.filter(user=request.user)
    return render(request, 'profile.html', {'favourites': favourites})


@login_required
def watch_history(request):
    watch_history = WatchHistory.objects.filter(user=request.user)
    return render(request, 'profile.html', {'watch_history': watch_history})

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        else:
            user_form = UserForm()
            profile_form = UserProfileForm()

        return render(request, 'register.html', {
            'user_form': user_form,
            'profile_form': profile_form,
            'registered': registered
        })
    
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect('AbsoluteCinema:home')
            else:
                return render(request, 'login.html', {'error': 'Your account is disabled.'})
        else:
            return render(request, 'login.html', {'error': 'Invalid login credentials.'})
    else:
        return render(request, 'login.html')
    
@login_required
def user_logout(request):
    logout(request)
    return redirect('AbsoluteCinema:index')

@login_required
def edit_profile(request):
    user_profile, _ = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect('AbsoluteCinema:profile')
    else:
        profile_form = UserProfileForm(instance=user_profile)

    return render(request, 'edit_profile.html', {'profile_form': profile_form})