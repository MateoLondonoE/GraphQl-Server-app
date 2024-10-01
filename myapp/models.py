from django.db import models

class Movie(models.Model):
    title = models.CharField(max_length=255)
    year = models.CharField(max_length=4)
    director = models.CharField(max_length=255)
    plot = models.TextField()
    imdb_rating = models.CharField(max_length=5)

    def __str__(self):
        return self.title
