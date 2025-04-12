from django.db import models


class AuthorBio(models.Model):
    link_site = models.URLField(max_length=250)  # Обычное строковое поле, но внутри которого уже есть проверки на валидность URL(если нет https:// - не URL)
    biography = models.TextField(null=True, blank=True)  # большое текстовое поле, ему не нужно указывать размерность как у CharField. настройки null и blank помогают задать возможность хранения NULL в базе данных и пропуска заполнения поля в JSON \ Admin панели соответственно
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Благодаря этому auto_now_add это поле будет помечено как неизменяемое, а дата и время будут ставиться автоматически в момент создания объекта, один раз и всё
    updated_at = models.DateTimeField(auto_now=True)  # А вот здесь auto_now скажет системе, что поле будет заполняться автоматически И ПРИ СОЗДАНИИ, И ПРИ ОБНОВЛЕНИИ, каждый раз

    def __str__(self):
        return f"{self.author.name[0]}. {self.author.surname}'s BIO"  # Rouling's BIO (Sapkivsky's BIO)

    class Meta:
        db_table = "author_bio"

class Author(models.Model):
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    bio = models.OneToOneField(  # Поле, позволяющее простроить связь O2O (One to One), тем самым настроив уникальность одного объекта относительно другого
        AuthorBio,  # тут мы указываем название класса с которым должна простроиться связь
        on_delete=models.PROTECT,  # обязательный параметр, мы указываем: что должно произойти со всеми вторичными объектами, если главный будет удалён (в нашем случае объекты защищены. Если профиль попробуют удалить - ничего не получится, пока на него ссылается какой-то автор)
        null=True,  # позволит нам заняться заполнением профиля уже после создания объекта автора
        blank=True,
        related_name='author'
    )

    def __str__(self):  # Переопределённый метод, который поможет нам видеть объекты в Админ панели не как Author object(1) и так далее, а как нормальное, описательное значение, например инициалы имени и фамилии, как у нас здесь
        return f"{self.name[0]}. {self.surname}"

    class Meta:
        db_table = "author"
