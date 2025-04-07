from django.contrib import admin

from books.models import Book, Author, AuthorBio  # импорт нужных моделей из нужного приложения

# в этом файле мы регистрируем те модели, которые нужны нам в работе в Админ панели по URL /admin

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'release_year', 'genre')
    search_fields = ('title', 'author__surname')
    list_filter = ('rating', 'release_year', 'language')
    list_per_page = 2


# class BookAdmin(admin.ModelAdmin):
#     list_display = ('title', 'author', 'release_year', 'genre')
#     search_fields = ('title', 'author__surname')
#     list_filter = ('rating', 'release_year', 'language')
#     list_per_page = 2


# admin.site.register(Book, BookAdmin)  # Регистрация модели книги
admin.site.register(Author)  # Регистрация модели автора
admin.site.register(AuthorBio)  # Регистрация модели профиля автора
