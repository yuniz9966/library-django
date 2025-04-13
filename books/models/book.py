from django.db import models

from books.models.author import Author
from books.models.user import User
from books.models.user import get_first_admin


class Book(models.Model):
    GENRE_CHOICES = [  # специальный список значений, из которых можно выбирать жанры для книг. Если нам подходит вариант, что у нас будет всего несколько значений, никаких обновлений, дополнений и удалений не планируется с ними - подходит. В противном случае мы могли бы создать отдельную модель жанров и соединять её с нашими книгами
        ('Fantasy', 'Fantasy'),
        ('Science', 'Science'),  # значения тут указываются в виде кортежа, где первая строчка - как нам будет предложено значение в Админ панели, а вторая - как значение будет записано в базе данных
        ('Cooking', 'Cooking'),
        ('Business', 'Business'),
        ('Psychology', 'Psychology'),
        ('History', 'History'),
    ]

    title = models.CharField(max_length=140)  # title VARCHAR(140)
    rating = models.FloatField(default=0.0)  # общий параметр, помогающий поставить значение по умолчанию, тогда поле явно заполнять не придётся
    genre = models.CharField(max_length=30, choices=GENRE_CHOICES)  # наше то самое строковое поле с возможностью выбора конкретных жанров
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

    def __str__(self):  # вместо нечитабельного book object(n) мы будем получать название книги в таблице книг в Админ панели
        return self.title

    class Meta:
        db_table = "book"
        verbose_name = "Book"
        verbose_name_plural = "Books"
        unique_together = ("title", "author")
        ordering = ("release_year",)
