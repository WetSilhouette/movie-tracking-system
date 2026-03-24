from  django.urls import path
from .views import (index, add_watch_later_movie, find_watch_later_movies_title,
                    find_movie_for_watched_title, find_watched_movies, add_watched_movie,
                    update_watched_movie, delete_watched_movie, find_watch_later_movies,
                    delete_watch_later_movie, move_to_watched)

urlpatterns = [
    path('', index, name='index'),
    path('add_watch_later_movie/', add_watch_later_movie, name='add_watch_later_movie'),
    path('find_watch_later_movies_title/', find_watch_later_movies_title, name='find_watch_later_movies_title'),
    path('find_movie_for_watched_title/', find_movie_for_watched_title, name='find_movie_for_watched_title'),
    path('watch_later_movies/', find_watch_later_movies, name='find_watch_later_movies'),
    path('watch_later_movies/delete/<int:movie_id>/', delete_watch_later_movie, name='delete_watch_later_movie'),
    path('watch_later_movies/move_to_watched/<int:movie_id>/', move_to_watched, name='move_to_watched'),
    path('watched_movies/', find_watched_movies, name='find_watched_movies'),
    path('add_watched_movie/', add_watched_movie, name='add_watched_movie'),
    path('watched_movies/update/<int:watched_movie_id>/', update_watched_movie, name='update_watched_movie'),
    path('watched_movies/delete/<int:watched_movie_id>/', delete_watched_movie, name='delete_watched_movie'),
]
