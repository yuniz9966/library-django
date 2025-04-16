from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from books.serializers import BookListSerializer, BookDetailSerializer, BookCreateSerializer
from books.models import Book


@api_view(['GET'])
def list_of_books(request) -> Response:
    books = Book.objects.all()  # Queryset[<Book obj1>, ..., <Book obj150>]

    serializer = BookListSerializer(books, many=True)

    return Response(
        data=serializer.data,
        status=200
    )


@api_view(['GET'])
def get_book_detail(request, book_id: int) -> Response:
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response(
            data={
                "message": "BOOK NOT FOUND"
            },
            status=404
        )

    serializer = BookDetailSerializer(book)

    return Response(
        data=serializer.data,
        status=200
    )


@api_view(['POST'])
def book_create(request):
    serializer = BookCreateSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['PUT'])
def update_book(request, book_id: int) -> Response:
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response(
            data={
                "message": "Book not found"
            },
            status=404
        )

    serializer = BookCreateSerializer(instance=book, data=request.data)

    if serializer.is_valid():
        serializer.save()

        return Response(
            data=serializer.data,
            status=200
        )

    else:
        return Response(
            data=serializer.errors,
            status=400
        )


@api_view(['DELETE'])
def delete_book(request, book_id: int) -> Response:
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return Response(
            data={
                "message": "Book not found"
            },
            status=404
        )

    book.delete()

    return Response(
        data={
            "message": "Book was deleted successfully."
        },
        status=204
    )
