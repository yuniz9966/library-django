from django.contrib import admin
from django.db.models import QuerySet
from django.utils import timezone

from books.models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'release_year', 'genre')
    search_fields = ('title', 'author__surname')
    list_filter = ('release_year', 'language')
    list_per_page = 15

    actions = ['update_release_year']

    def update_release_year(self, request, objects: QuerySet) -> None:
        for obj in objects:
            obj.release_year = timezone.now()

            obj.save()

    update_release_year.short_description = "Обновить дату релиза"
