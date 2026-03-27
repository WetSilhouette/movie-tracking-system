# Movie Tracking System

A Django-based web application for managing your movie watchlist and tracking watched movies. This system integrates with The Movie Database (TMDB) API to fetch movie information and provides an intuitive interface for organizing your movie collection.

## Features

- 📋 **Watch Later List**: Add movies you want to watch in the future
- ✅ **Watched Movies**: Track movies you've already watched with personal ratings and dates
- 🔍 **TMDB Integration**: Automatically fetch movie details including:
  - Title, release year, and director
  - General ratings and vote counts
  - Movie descriptions and genres
  - Poster images
- 📊 **Dashboard**: View statistics and recent activity at a glance
- ✏️ **Edit & Update**: Modify your ratings and watched dates
- 🔄 **Move Movies**: Easily move movies from "Watch Later" to "Watched"

## Tech Stack

- **Backend**: Django 6.0.3
- **Database**: SQLite
- **API**: The Movie Database (TMDB) API
- **Frontend**: HTML, CSS (custom styles)
- **Python**: 3.13+

## Project Structure

```
movie-recommendation-system/
├── movies/                 # Main Django app
│   ├── models.py          # Movie and WatchedMovie models
│   ├── views.py           # View functions and business logic
│   ├── urls.py            # URL routing
│   ├── templates/         # HTML templates
│   └── static/            # CSS and static files
├── mysite/                # Django project settings
│   ├── settings.py        # Project configuration
│   └── urls.py            # Root URL configuration
├── manage.py              # Django management script
├── pyproject.toml         # Project dependencies
└── README.md              # This file
```

## Installation

### Prerequisites

- Python 3.13 or higher
- TMDB API key (get one at [https://www.themoviedb.org/settings/api](https://www.themoviedb.org/settings/api))

### Setup Steps

1. **Clone the repository**
   ```bash
   cd movie-recommendation-system
   ```

2. **Install dependencies**
   ```bash
   pip install django requests python-dotenv
   ```

3. **Set up environment variables**

   Create a `.env` file in the project root:
   ```
   TMDB_API_KEY=your_api_key_here
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the development server**
   ```bash
   python manage.py runserver
   ```

6. **Access the application**

   Open your browser and navigate to `http://127.0.0.1:8000/`

## Usage

### Adding Movies to Watch Later

1. Navigate to "Add Watch Later Movie"
2. Search for a movie by title
3. The system will fetch movie details from TMDB
4. Review and save the movie to your watch later list

### Marking Movies as Watched

**Option 1: From Watch Later List**
- Go to your "Watch Later" list
- Click "Move to Watched" on any movie
- Add your rating and watched date

**Option 2: Add Directly**
- Navigate to "Add Watched Movie"
- Search for a movie by title
- Add your rating and watched date
- Save to your watched movies list

### Managing Your Collection

- **View Watched Movies**: See all movies you've watched with your ratings
- **Update Ratings**: Edit your personal rating or watched date
- **Delete Movies**: Remove movies from either list
- **Dashboard**: View statistics including:
  - Total movies in database
  - Watch later count
  - Watched movies count
  - Recent activity

## Database Models

### Movie
- `title`: Movie title
- `release_year`: Year of release
- `director`: Director name
- `general_rating`: TMDB average rating
- `total_ratings`: Number of TMDB votes
- `description`: Movie overview
- `keywords`: Genres/keywords
- `tmdb_id`: TMDB movie ID
- `tmdb_poster_path`: Poster image path
- `watch_later`: Boolean flag for watch later status

### WatchedMovie
- `movie`: Foreign key to Movie
- `my_rating`: Your personal rating
- `watched_date`: Date you watched the movie


