from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=140)  # title VARCHAR(140)
    rating = models.FloatField()
    genre = models.CharField(max_length=30)
    release_year = models.DateField() #  2011-05-05
    author = models.CharField(
        max_length=50
    )
    pages = models.SmallIntegerField()
    language = models.CharField(max_length=15)
    isbn = models.CharField(max_length=50)
