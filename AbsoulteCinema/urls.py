from django.urls import path
from . import views

app_name = 'AbsoluteCinema'

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('movies/', views.movies, name='movies'),
    path('movies/<int:movie_id>/', views.movie_detail, name='movie_detail'),
    path('profile/', views.profile, name='profile'),
]