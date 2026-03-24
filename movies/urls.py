from  django.urls import path
from .views import index, add_watch_later_movie, find_watch_later_movies_title, find_movie_for_watched_title, find_watched_movies, add_watched_movie

urlpatterns = [
    path('', index, name='index'),
    path('add_watch_later_movie/', add_watch_later_movie, name='add_watch_later_movie'),
    path('find_watch_later_movies_title/', find_watch_later_movies_title, name='find_watch_later_movies_title'),
    path('find_movie_for_watched_title/', find_movie_for_watched_title, name='find_movie_for_watched_title'),
    path('watched_movies/', find_watched_movies, name='find_watched_movies'),
    path('add_watched_movie/', add_watched_movie, name='add_watched_movie'),
]
