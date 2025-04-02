from django.db import models


class AuthorBio(models.Model):
    link_site = models.URLField(max_length=250)  # Обычное строковое поле, но внутри которого уже есть проверки на валидность URL(если нет https:// - не URL)
    biography = models.TextField(null=True, blank=True)  # большое текстовое поле, ему не нужно указывать размерность как у CharField. настройки null и blank помогают задать возможность хранения NULL в базе данных и пропуска заполнения поля в JSON \ Admin панели соответственно
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Благодаря этому auto_now_add это поле будет помечено как неизменяемое, а дата и время будут ставиться автоматически в момент создания объекта, один раз и всё
    updated_at = models.DateTimeField(auto_now=True)  # А вот здесь auto_now скажет системе, что поле будет заполняться автоматически И ПРИ СОЗДАНИИ, И ПРИ ОБНОВЛЕНИИ, каждый раз


class Author(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    bio = models.OneToOneField(  # Поле, позволяющее простроить связь O2O (One to One), тем самым настроив уникальность одного объекта относительно другого
        AuthorBio,  # тут мы указываем название класса с которым должна простроиться связь
        on_delete=models.PROTECT,  # обязательный параметр, мы указываем: что должно произойти со всеми вторичными объектами, если главный будет удалён (в нашем случае объекты защищены. Если профиль попробуют удалить - ничего не получится, пока на него ссылается какой-то автор)
        null=True  # позволит нам заняться заполнением профиля уже после создания объекта автора
    )

    def __str__(self):  # Переопределённый метод, который поможет нам видеть объекты в Админ панели не как Author object(1) и так далее, а как нормальное, описательное значение, например инициалы имени и фамилии, как у нас здесь
        return f"{self.name[0]}. {self.surname}"


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
        null=True  # это значение позволит нам создавать книгу, не указывая автора сразу
    )
    pages = models.SmallIntegerField(null=True, blank=True)
    language = models.CharField(max_length=15, default="English")
    isbn = models.CharField(max_length=50)

    def __str__(self):  # вместо нечитабельного book object(n) мы будем получать название книги в таблице книг в Админ панели
        return self.title
