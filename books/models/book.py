from django.db import models

from books.models.author import Author
from books.models.user import User
from books.models.genres import Genre
from books.models.user import get_first_admin
from django.utils import timezone

from books.managers.books import SoftDeleteManager


class Book(models.Model):
    title = models.CharField(max_length=140)  # title VARCHAR(140)
    rating = models.FloatField(default=0.0)  # общий параметр, помогающий поставить значение по умолчанию, тогда поле явно заполнять не придётся
    genre = models.ForeignKey(
        Genre,
        related_name='books',
        on_delete=models.PROTECT
    )
    release_year = models.DateField()  # 2011-05-05 DATE
    author = models.ForeignKey(  # поле для создания связи O2M (One to Many) связи
        Author,  # так же указываем название класса с которым создаём связь
        on_delete=models.CASCADE,  # опять же, обязательный параметр. В нашем случае если вдруг какой-то автор будет удалён - все его книги, которые он писал, будут каскадно удалены в базе
        null=True,  # это значение позволит нам создавать книгу, не указывая автора сразу
        related_name="books"
    )
    publisher = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="books",
        default=get_first_admin
    )
    price = models.DecimalField(max_digits=6, decimal_places=4, default=0.0)
    discounted_price = models.DecimalField(max_digits=6, decimal_places=4, default=0.0)
    pages = models.SmallIntegerField(null=True, blank=True)
    language = models.CharField(max_length=15, default="English")
    isbn = models.CharField(max_length=50)
    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.deleted_at = timezone.now()

        self.save()

    def __str__(self):  # вместо нечитабельного book object(n) мы будем получать название книги в таблице книг в Админ панели
        return self.title

    class Meta:
        db_table = "book"
        verbose_name = "Book"
        verbose_name_plural = "Books"
        unique_together = ("title", "author")
        ordering = ("release_year",)
