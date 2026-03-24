from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Movie, Review, Favourite, WatchHistory


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