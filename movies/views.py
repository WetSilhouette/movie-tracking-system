import os

import requests
from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie, WatchedMovie
from dotenv import load_dotenv
import os

load_dotenv()

def index(request):
    # Get statistics for the dashboard
    watch_later_count = Movie.objects.filter(watch_later=True).count()
    watched_count = WatchedMovie.objects.count()
    total_movies = Movie.objects.count()

    # Get recent watched movies (last 5)
    recent_watched = WatchedMovie.objects.all().order_by('-watched_date')[:5]

    # Get recent watch later movies (last 5)
    recent_watch_later = Movie.objects.filter(watch_later=True).order_by('-id')[:5]

    context = {
        'watch_later_count': watch_later_count,
        'watched_count': watched_count,
        'total_movies': total_movies,
        'recent_watched': recent_watched,
        'recent_watch_later': recent_watch_later,
    }

    return render(request, "index.html", context)

def add_watch_later_movie(request):
    if request.method == "POST":
        title = request.POST["title"]
        release_year = request.POST["release_year"]
        director = request.POST["director"]
        general_rating = request.POST["general_rating"]
        total_ratings = request.POST["total_ratings"]
        description = request.POST["description"]
        keywords = request.POST["keywords"]
        tmdb_id = request.POST["tmdb_id"]
        tmdb_poster_path = request.POST["tmdb_poster_path"]
        movie = Movie(title=title, release_year=release_year, director=director, general_rating=general_rating, total_ratings=total_ratings,
                      description=description, keywords=keywords, tmdb_id=tmdb_id, tmdb_poster_path=tmdb_poster_path, watch_later=True)
        if movie.title in Movie.objects.values_list('title', flat=True):
            return render(request, "add_watch_later_movie.html", {'error': True, 'error_message': 'Movie already in list.'})
        else:
            movie.save()
            print(f"Movie: {movie}")
        return render(request, "add_watch_later_movie.html", {'success': True})
    return render(request, "add_watch_later_movie.html")

def find_movie(request, html_template: str):
    if request.method == "GET" and "title" in request.GET:
        title = request.GET["title"]
        movie = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={os.getenv('TMDB_API_KEY')}&query={title}").json()
        if movie["results"]:
            movie_data = movie["results"][0]
            # Get additional details including director
            movie_id = movie_data["id"]
            details = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={os.getenv('TMDB_API_KEY')}&append_to_response=credits").json()

            # Extract director from credits
            director = "Unknown"
            if "credits" in details and "crew" in details["credits"]:
                for crew_member in details["credits"]["crew"]:
                    if crew_member["job"] == "Director":
                        director = crew_member["name"]
                        break

            # Extract keywords from genres
            keywords = ""
            if details.get("genres"):
                keywords = ", ".join([genre["name"] for genre in details.get("genres", [])])

            # Prepare data for template
            context = {
                'movie_found': True,
                'title': movie_data.get("title", ""),
                'release_year': movie_data.get("release_date", "")[:4] if movie_data.get("release_date") else "",
                'director': director,
                'general_rating': movie_data.get("vote_average", 0),
                'total_ratings': movie_data.get("vote_count", 0),
                'description': movie_data.get("overview", ""),
                'keywords': keywords,
                'tmdb_id': movie_data.get("id", ""),
                'tmdb_poster_path': movie_data.get("poster_path", ""),
            }
            print(f"Context: {context}")
            return render(request, html_template, context)
        else:
            return render(request, html_template, {'error': True, 'error_message': 'Movie not found in TMDB'})
    return render(request, html_template)

def find_watch_later_movies_title(request):
    return find_movie(request, "add_watch_later_movie.html")

def find_movie_for_watched_title(request):
    return find_movie(request, "add_watched_movie.html")

def add_watched_movie(request):
    if request.method == "POST":
        title = request.POST["title"]
        release_year = request.POST["release_year"]
        director = request.POST["director"]
        general_rating = request.POST["general_rating"]
        total_ratings = request.POST["total_ratings"]
        description = request.POST["description"]
        keywords = request.POST["keywords"]
        tmdb_id = request.POST["tmdb_id"]
        tmdb_poster_path = request.POST["tmdb_poster_path"]
        watched_date = request.POST["watched_date"]
        my_rating = request.POST["my_rating"]
        movie = Movie(title=title, release_year=release_year, director=director, general_rating=general_rating, total_ratings=total_ratings,
                      description=description, keywords=keywords, tmdb_id=tmdb_id, tmdb_poster_path=tmdb_poster_path, watch_later=False)
        if movie.title in Movie.objects.values_list('title', flat=True):
            movie = Movie.objects.get(title=movie.title)
            movie.watch_later = False
            movie.save()
            if not WatchedMovie.objects.filter(movie=movie).exists():
                WatchedMovie(movie=movie, watched_date=watched_date, my_rating=my_rating).save()
            return render(request, "add_watched_movie.html", {'success': True, 'success_message': 'Movie changed status from Watch Later to Watched successfully!'})
        else:
            movie.save()
            if not WatchedMovie.objects.filter(movie=movie).exists():
                WatchedMovie(movie=movie, watched_date=watched_date, my_rating=my_rating).save()
            return render(request, "add_watched_movie.html", {'success': True, 'success_message': 'Movie added to watched movies successfully!'})
    return render(request, "add_watched_movie.html", {'error': True, 'error_message': 'Movie not found in TMDB'})

def find_watched_movies(request):
    watched_movies = WatchedMovie.objects.all()
    return render(request, "watched_movies.html", {'watched_movies': watched_movies})


def update_watched_movie(request, watched_movie_id):
    watched_movie = get_object_or_404(WatchedMovie, id=watched_movie_id)

    if request.method == "POST":
        watched_movie.my_rating = request.POST.get("my_rating")
        watched_movie.watched_date = request.POST.get("watched_date")
        watched_movie.save()
        return redirect('find_watched_movies')

    context = {
        'watched_movie': watched_movie,
        'movie': watched_movie.movie
    }
    return render(request, "update_watched_movie.html", context)

def delete_watched_movie(request, watched_movie_id):
    watched_movie = get_object_or_404(WatchedMovie, id=watched_movie_id)

    if request.method == "POST":
        movie = watched_movie.movie
        watched_movie.delete()

        # If no other WatchedMovie references this movie, optionally delete the movie too
        # or mark it as watch_later again
        if not WatchedMovie.objects.filter(movie=movie).exists():
            # Option 1: Delete the movie entirely
            # movie.delete()

            # Option 2: Mark as watch later again
            movie.watch_later = True
            movie.save()

        return redirect('find_watched_movies')

    context = {
        'watched_movie': watched_movie
    }
    return render(request, "delete_watched_movie.html", context)


def find_watch_later_movies(request):
    watch_later_movies = Movie.objects.filter(watch_later=True)
    return render(request, "watch_later_movies.html", {'watch_later_movies': watch_later_movies})

def delete_watch_later_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == "POST":
        movie.delete()
        return redirect('find_watch_later_movies')

    context = {
        'movie': movie
    }
    return render(request, "delete_watch_later_movie.html", context)

def move_to_watched(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)

    if request.method == "POST":
        watched_date = request.POST.get("watched_date")
        my_rating = request.POST.get("my_rating")

        movie.watch_later = False
        movie.save()

        if not WatchedMovie.objects.filter(movie=movie).exists():
            WatchedMovie.objects.create(movie=movie, watched_date=watched_date, my_rating=my_rating)

        return redirect('find_watched_movies')

    context = {
        'movie': movie
    }
    return render(request, "move_to_watched.html", context)

