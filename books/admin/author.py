from django.contrib import admin

from books.models import Author, AuthorBio


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    ...

class AuthorInline(admin.StackedInline):
    model = Author
    extra = 1


@admin.register(AuthorBio)
class AuthorBioAdmin(admin.ModelAdmin):
    inlines = [AuthorInline]

    list_display = ('author_fullname', 'date_of_birth', 'short_bio')

    def short_bio(self, obj: AuthorBio) -> str:
        return f"{obj.biography[:30]}..."

    def author_fullname(self, obj: AuthorBio) -> str:
        return f"{obj.author.name[0]}. {obj.author.surname}"
