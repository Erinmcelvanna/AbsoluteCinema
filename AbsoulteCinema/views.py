from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .models import Movie, Review, Favourite, WatchHistory, Rating


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