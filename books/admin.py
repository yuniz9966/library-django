from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from books.models import Book, Author, AuthorBio, User  # импорт нужных моделей из нужного приложения

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


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password', 'role')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone', 'birth_day')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'role')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)



admin.site.unregister(Group)
admin.site.register(Group)
# admin.site.register(Book, BookAdmin)  # Регистрация модели книги
admin.site.register(Author)  # Регистрация модели автора
admin.site.register(AuthorBio)  # Регистрация модели профиля автора
