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


# ===========================================================================================================
# ===========================================================================================================

# ORM QUERIES PART II

# ===========================================================================================================
# ===========================================================================================================


# from books.models import Book
# from django.db.models import Count, Avg
#
# result = Book.objects.aggregate(
#     total_books=Count('id'),
#     avg_price=Avg('price')
# )
#
# print(result)

# print(f"Общее кол-во книг = {result['total_books']}")
# print(f"Средняя цена книг = {round(result['avg_price'], 2)}")


# ======================================================================


# from books.models import Book
# from django.db.models import Count
#
# # author_books = Book.objects.values('author') # -> QuerySet[{'author': ...}, {}]
# author_books = Book.objects.values('author').annotate(
#     books_count=Count('id')
# )  # -> SELECT author, count(id) as books_count FROM books GROUP BY author;
#
# print("="*100)
# print(author_books.query)
# print("="*100)
# print(author_books)


# =================================================================================

# ORDER BY

# from books.models import Book


# sorted_books = Book.objects.order_by('-title')
#
# # print(sorted_books)
# print(sorted_books.query)
#
# for book in sorted_books:
#     print(book.id, book.title)


# ORDER BY По нескольким полям

# from books.models import Book
#
# sorted_books = Book.objects.order_by(
#     'author__name',
#     'title'
# )
#
# print(sorted_books.query)
#
# for book in sorted_books:
#     print(book.author, book.title)


# from books.models import Book
#
#
# books = Book.objects.all()[7:8]
#
# print(books.query)
#
# for b in books:
#     print(b.id, b.title)


# -----------------------------------------------------------------------


# SUBQUERIES

# from django.db.models import Avg
#
# from books.models import Book
#
# avg_price_subq = Book.objects.aggregate(
#     avg_price=Avg('price')  # -> {"avg_price": 22.102371}
# )['avg_price']
#
# filtered_books = Book.objects.filter(
#     price__lte=avg_price_subq
# )
#
#
# print(filtered_books.query)
#
# for book in filtered_books:
#     print(book.id, book.title, round(book.price, 2), round(avg_price_subq, 2))


# ------------------------------------------------------------------

# from django.db.models import Subquery, OuterRef, Min
#
# from books.models import Book
#
#
# subquery = (
#     Book.objects.filter(author=OuterRef('author')) # SELECT * ...
#     .values('author')  # SELECT book.author_id ...
#     .annotate(min_price=Min('price'))  # SELECT book.author_id, min(price) as min_price ...
#     .values('min_price') # SELECT min(price) as min_price FROM book AS U0 WHERE UO.author_id = book.author_id GROUP BY U0.author_id
# )
#
# main_query = Book.objects.annotate(min_price_by_author=Subquery(subquery))
# # SELECT *, SUBQUERY(...) as min_price_by_author
#
# print(main_query.query)


# from django.db.models import OuterRef, Subquery, Avg
#
# from books.models import Book
#
#
# # Подзапрос для вычисления средней цены книги того же издательства
# subquery = (
#     Book.objects.filter(publisher=OuterRef('publisher'))
#     .values('publisher')
#     .annotate(avg_price=Avg('price'))
#     .values('avg_price')[:1]
# )
#
#
# # Фильтрация книг с ценой ниже средней цены для их издательства
# books_below_average = Book.objects.filter(price__lt=Subquery(subquery))
# print(books_below_average.query)
#
# for book in books_below_average:
#     print(book.title, book.price)


# -------------------------------------------------------------------------------


# EXPRESSION WRAPPER

# from django.db.models import ExpressionWrapper, F, fields
#
# from books.models import Book
#
#
# data = Book.objects.annotate(
#     comission_price=ExpressionWrapper(
#         expression=F('price') * 1.18,
#         output_field=fields.FloatField()
#     )
# )
#
# print(data)


# ---------------------------------------------------------------------------

# DJANGO DRF

# my_dict = {...} -> SERIALIZER(my_dict) -> "{...}" # Сериализация
#
# "{...}" -> SERIALIZER("{...}") -> {...} # Десериализация


# from books.serializers import BookSerializer
#
# from django.utils import timezone
#
# data = {
#     "title": "TEST TITLE",
#     "rating": 10.02,
#     "pages": 255,
#     "release_year": timezone.now().date(),
# }
#
#
# book_serializer = BookSerializer(data=data)
#
# book_serializer.is_valid()
#
# print(book_serializer.errors)
# print(book_serializer.validated_data)

# print(book_serializer)


# =======================================================


# from books.models import Book
#
#
# all_books = Book.objects.all()
# print(all_books.query)
#
# upd_queryset = all_books.filter(
#     genre=1
# )
# print(upd_queryset.query)
#
#
# print(upd_queryset[0].genre)


# from books.debug_tools import QueryDebug
# from books.models import Book
#
#
# all_books = Book.objects.select_related(
#     'publisher', 'author', 'genre'
# ).all()
#
# print(all_books.query)
#
#
# with QueryDebug(file_name='queries.log') as qd:
#     for b in all_books:
#         print(b.id, b.publisher.email, b.author.surname, b.genre.name)


# from books.debug_tools import QueryDebug
# from books.models import Book, Author
# from django.db.models import Prefetch
#
#
# authors = Author.objects.all()
#
# print(authors.query)
#
# with QueryDebug(file_name='queries.log') as qd:
#     for a in authors:
#         print(a.surname)
#         for b in a.books.all():
#             print(b.title, b.publisher.email, b.genre.name)


# authors = Author.objects.prefetch_related(
#     Prefetch(
#         'books',
#         queryset=Book.objects.select_related(
#             'genre', 'publisher'
#         )
#     )
# )
#
# print(authors.query)
#
# with QueryDebug(file_name='queries.log') as qd:
#     for a in authors:
#         print(a.surname)
#         for b in a.books.all():
#             print(b.title, b.publisher.email, b.genre.name)



from books.models import Book, Genre, User, Author
from django.db.models import QuerySet
from books.debug_tools import QueryDebug


all_books: QuerySet = Book.objects.select_related(
    'genre', 'publisher', 'author'
)


with QueryDebug(file_name='db_logs_sum_7.log') as qd:
    for b in all_books:
        print(b.title, b.rating, b.genre, b.publisher, b.author)
