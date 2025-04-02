from django.contrib import admin

from books.models import Book, Author, AuthorBio  # импорт нужных моделей из нужного приложения

# в этом файле мы регистрируем те модели, которые нужны нам в работе в Админ панели по URL /admin


admin.site.register(Book)  # Регистрация модели книги
admin.site.register(Author)  # Регистрация модели автора
admin.site.register(AuthorBio)  # Регистрация модели профиля автора
