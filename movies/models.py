from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    release_year = models.IntegerField()
    director = models.CharField(max_length=255)
    general_rating = models.FloatField()
    total_ratings = models.IntegerField()
    description = models.TextField()
    keywords = models.CharField(max_length=255)
    tmdb_id = models.IntegerField()
    tmdb_poster_path = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class WatchedMovie(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    my_rating = models.FloatField(null=True)
    watched_date = models.DateField()


