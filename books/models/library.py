from django.db import models

from books.models.book import Book


class Library(models.Model):
    name = models.CharField(max_length=120, unique=True)
    postal_code = models.CharField(max_length=20)
    slug = models.SlugField(unique=True, blank=True)
    books = models.ManyToManyField(Book, related_name='libraries')

    class Meta:
        verbose_name = 'Library'
        verbose_name_plural = 'Libraries'

    def __str__(self):
        return self.name
