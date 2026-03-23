from  django.urls import path
from .views import index, add_movie, find_movie, find_watched_movies
urlpatterns = [
    path('', index, name='index'),
    path('add_movie/', add_movie, name='add_movie'),
    path('find_movie/', find_movie, name='find_movie'),
    path('watched_movies/', find_watched_movies, name='find_watched_movies'),
]
