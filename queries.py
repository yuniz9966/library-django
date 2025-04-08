import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')
django.setup()


from books.models import Book


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

book = Book.objects.get(genre="qwerqwerqwer")

print(book)
