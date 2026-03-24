from django.urls import path
from . import views

app_name = 'AbsoluteCinema'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('movies/', views.movies, name='movies'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('movies/<int:movie_id>/rate/', views.add_rating, name='add_rating'),
    path('movies/<int:movie_id>/reviews/', views.add_review, name='add_review'),
    path('ranked/', views.ranked, name='ranked'),
    path('profile/', views.profile, name='profile'),
    path('profile/favourites/', views.favourites, name='favourites'),
    path('profile/watch-history/', views.watch_history, name='watch_history'),
]