import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')
django.setup()

# all_books = Book.objects.all()  # SELECT * FROM book;

# print(all_books.query)
# print(all_books)
#
# for book in all_books:
#     print(book.title)

# from datetime import datetime
#
# book = Book.objects.create(
#     title="Django Test ORM Query Result",
#     rating=5.98,
#     genre="Fiction",
#     release_year=datetime.strptime("2005-07-09", "%Y-%m-%d"),
#     isbn="1234-4342-4564-5675"
# )
#
# print("Книга создана")
#
# new_book = Book(
#     title="Django Test ORM Query Result",
#     rating=5.98,
#     genre="Fiction",
#     release_year=datetime.strptime("2005-07-09", "%Y-%m-%d"),
#     isbn="1234-4342-4564-5675"
# )
#
#
# new_book.pages = 433
#
# new_book.save()

# first_book = Book.objects.first()
#
# if first_book:
#     print(first_book.id, first_book.title)
# else:
#     print("NOT FOUND")


# first_book = Book.objects.last()
#
# if first_book:
#     print(first_book.id, first_book.title)
# else:
#     print("NOT FOUND")


# books_count = Book.objects.all().count()
#
# print(f"Кол-во книг = {books_count}")


# books_count = Book.objects.all().exists()

# print(f"Кол-во книг = {books_count}")

# books = Book.objects.all().values('title', 'rating')
#
# print(books.query)
#
# for book in books:
#     print(book['title'], book['rating'])

# book = Book.objects.get(genre="qwerqwerqwer")
#
# print(book)


# req_books = Book.objects.filter(
#     rating=8.2,
#     language="English"
#
# )
#
# print(req_books)

# req_books = Book.objects.filter(
#     rating__gt=8.2,
#     language="English"
# )
#
# print(req_books)


# req_books = Book.objects.filter(
#     title__icontains="ReaLitY"
# )
#
# print(req_books)


# req_books = Book.objects.filter(
#     id__in=[2, 4, 6, 10]
# )
#
# print(req_books)

# req_books = Book.objects.filter(
#     release_year__gt="2002-06-21"
# )
#
# print(req_books)

# req_books = Book.objects.filter(
#     release_year__gte="2002-06-21"
# )
#
# print(req_books)


# req_books = Book.objects.filter(
#     release_year__range=["2001-09-16", "2002-06-21"]
# )
#
# print(req_books)


# req_books = Book.objects.filter(
#     title__istartswith="the"
# )
#
# print(req_books)


# req_books = Book.objects.filter(
#     title__endswith="ing"
# )
#
# print(req_books)


# req_books = Book.objects.filter(
#     title__endswith="ing"
# )
#
# print(req_books)

from django.db.models import Q

# req_books = Book.objects.filter(
#     genre="Psychology",
#     release_year__gte="2002-09-06"
# )
#
# print(req_books)


# req_books = Book.objects.filter(
#     (Q(genre="Psychology") & Q(release_year__gte="2002-09-06")) | Q(rating__gt=4)
# )
#
# print(req_books)


# books = Book.objects.filter(
#     ~Q(language="French")
# )
#
# print(books)
#
# for b in books:
#     print(b.language)

# from django.db.models import Q
#
# books = Book.objects.filter(
#     (Q(genre="Fantasy") | Q(rating__lte=6)) & ~Q(release_year="2009-03-20")
# )
#
# print(books)

# =================================================================
# =================================================================
# =================================================================

# book = Book.objects.get(id=152)
# book.pages = 293
#
# book.save()


# Book.objects.filter(genre="Business").update(
#     rating=8.88
# )


# ==========================================================
# ==========================================================
# ==========================================================

from django.db.models import F


# Book.objects.filter(id__in=[1, 2, 3]).update(rating=F('rating') - 1)

# Book.objects.filter(id__in=[1,]).update(title=F('title') + "( SSS)")

# Book.objects.update(price=22.45)


# Book.objects.update(
#     discounted_price=F('price') * 0.8
# )


# Book.objects.get(title="Django Test ORM Query Result").delete()

# deleted, _ = Book.objects.filter(rating=1.1).delete()
#
# print(f"Удалено {deleted} записей -> {_}")

# def delete():
#     return count_deleted_objects, delete_details

# def return_tuple() -> tuple[str, str]:
#     return "FIRST", "SECOND"
#
# first, second = return_tuple()
#
# print(first, second)

# for _ in range(10):
#     print("HELLO")

# from books.models import User
#
# user = User(
#     username="NEWUniqueUser",
#     email="newunique.email@gmail.com",
#     first_name="Unique2",
#     last_name="User2",
# )
# user.set_password("as-0dG<y0S8^d7fgtS<78")
#
# user.save()


# books = Book.objects.all().values('title', 'genre', 'release_year')
# books = Book.objects.all() -> SELECT * FROM books;
# books = Book.objects.all().values('title') -> SELECT title FROM books;

# print(books)
#
# first_book = books.first()
# last_book = books.last()

# print(first_book)
# print(last_book)
# print(books.exists())
#
# print(books.query)


# req_book = Book.objects.get(genre="qwerqwerqwerqwer")
# # SELECT * FROM books WHERE title = 'Home century';
#
# print(req_book)


# req_books = Book.objects.filter(
#     author__surname__startswith="S"
# )
#
# print(req_books.query)
# print(req_books)
#
# book = Book.objects.filter(
#     rating__gte=5.7
# )

# from django.db.models import F
#
# bad_discount_books = Book.objects.filter(
#     discounted_price__gt=F('price')
# ).update(discounted_price=F('price') * .7)
#
# print(bad_discount_books.query)
#
# print(bad_discount_books)
#
#
# # bad_discount_books = Book.objects.filter(
# #     discounted_price__gt=22.45
# # )
#
# Book.objects.filter(language="Russian").update(
#     rating=F('rating') + 1
# )


