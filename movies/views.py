import os

import requests
from django.shortcuts import render
from .models import Movie
from dotenv import load_dotenv
import os

load_dotenv()

def index(request):
    return render(request, "index.html")

def add_movie(request):
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
        movie = Movie(title=title, release_year=release_year, director=director, general_rating=general_rating, total_ratings=total_ratings, description=description, keywords=keywords, tmdb_id=tmdb_id, tmdb_poster_path=tmdb_poster_path)
        print(f"Movie: {movie}")
        movie.save()
        return render(request, "add_movie.html", {'success': True})
    return render(request, "add_movie.html")

def find_movie(request):
    if request.method == "GET" and "title" in request.GET:
        title = request.GET["title"]
        movie = requests.get(f"https://api.themoviedb.org/3/search/movie?api_key={os.getenv('TMDB_API_KEY')}&query={title}").json()
        if movie["results"]:
            movie_data = movie["results"][0]
            # Get additional details including director
            movie_id = movie_data["id"]
            details = requests.get(f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={os.getenv('TMDB_API_KEY')}&append_to_response=credits").json()
            print(f"Details: {details}")

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
            return render(request, "add_movie.html", context)
        else:
            return render(request, "add_movie.html", {'error': True, 'error_message': 'Movie not found in TMDB'})
    return render(request, "add_movie.html")

def find_watched_movies(request):
    watched_movies = Movie.objects.filter(watchedmovie__isnull=False)
    return render(request, "watched_movies.html", {'watched_movies': watched_movies})

