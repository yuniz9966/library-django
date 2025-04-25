from typing import Any

from django.db.models import QuerySet, Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, filters
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework import mixins
from rest_framework.decorators import action

from books.models import Genre
from books.serializers import GenreSerializer



class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    @action(
        detail=False,
        methods=['get',],
        url_path='statistic'
    )
    def get_books_count_by_genre(self, request: Request) -> Response:
        genres_statistic = Genre.objects.annotate( # SELECT *, count(books) as books_count FROM genre GROUP BY id;
            books_count=Count('books')
        )  # QuerySet[{"id": 1, "name": "Fantasy", "books_count": 45}, ...]

        data = [
            {
                "id": g.id,
                "name": g.name,
                "books_count": g.books_count,
            }
            for g in genres_statistic
        ]

        return Response(
            data=data,
            status=status.HTTP_200_OK
        )

from books.serializers import (
    BookListSerializer,
    BookDetailSerializer,
    BookCreateSerializer
)
from books.models import Book


class BooksByRegularIsbn(ListAPIView):
    serializer_class = BookListSerializer

    def get_queryset(self):
        queryset = Book.objects.filter(
            isbn=self.kwargs.get("isbn")
        )
        return queryset


# @api_view(['GET'])
# def list_of_books(request) -> Response:
#     books = Book.objects.all()  # Queryset[<Book obj1>, ..., <Book obj150>]
#
#     serializer = BookListSerializer(books, many=True)
#
#     return Response(
#         data=serializer.data,
#         status=200
#     )

class BooksListCreateView(ListCreateAPIView):
    queryset = Book.objects.all()

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['author__surname', 'publisher__email', 'genre']
    search_fields = ['title']
    ordering_fields = ['price', 'release_year']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookListSerializer
        return BookCreateSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()

        context['include_related'] = self.request.query_params.get(
            "include_related",
            "false"
        ).lower() == "true"

        return context

    # def get_queryset(self):
    #     queryset = Book.objects.all()
    #     # http://localhost:8000/books/?author=Johnson
    #     author_surname = self.request.query_params.get('author')
    #
    #     if author_surname:
    #         queryset = queryset.filter(
    #             author__surname__iexact=author_surname
    #         )
    #
    #     return queryset




# class BooksListCreateAPIView(APIView, PageNumberPagination):
#     page_size = 5
#
#     def get_queryset(self, request: Request):
#         allowed_sort_fields = {'rating', 'price', 'release_year'}
#
#         queryset: QuerySet[Book] = Book.objects.all()  # Queryset[<Book obj1>, ..., <Book obj150>]
#         # http://127.0.0.1:8000/books/?author=Smith&year=2008
#
#         # # http://127.0.0.1:8000/books/?author=Brooks&author=Levy
#         # authors = request.query_params.getlist('author') #  { "author": ["Brooks", "Levy"] }
#
#         # http://127.0.0.1:8000/books/?author=Brooks
#         # FILTER PARAMS
#         authors = request.query_params.getlist('author') #  { "author": ["Brooks",] }
#         year = request.query_params.get('year')
#
#         # SORT PARAMS
#         sort_by = request.query_params.get('sort_by', 'rating')
#         sort_order = request.query_params.get('order', 'asc')
#
#         if authors:
#             queryset = queryset.filter(
#                 author__surname__in=authors  # SELECT * FROM books WHERE author.surname IN ("Brooks", "Levy")
#             )
#
#         if year:
#             try:
#                 year = int(year)  # ?year=twenty two
#                 queryset = queryset.filter(
#                     release_year__year=year
#                 )
#             except ValueError:
#                 queryset = queryset.none()
#
#         if sort_by not in allowed_sort_fields:
#             sort_by = 'rating'
#
#         if sort_order == 'desc':
#             sort_by = f"-{sort_by}"
#
#         queryset = queryset.order_by(sort_by)
#
#         return queryset
#
#     def get_page_size(self, request):
#         page_size = request.query_params.get('page_size')
#
#         if page_size and page_size.isdigit():
#             return int(page_size)
#
#         return self.page_size
#
#
#     def get(self, request: Request) -> Response:
#         books = self.get_queryset(request=request)
#         results = self.paginate_queryset(queryset=books, request=request, view=self)
#         serializer = BookListSerializer(results, many=True)
#
#         return self.get_paginated_response(data=serializer.data)
#
#     def post(self, request: Request) -> Response:
#         serializer = BookCreateSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()  # create()
#             return Response(
#                 data=serializer.data,
#                 status=status.HTTP_201_CREATED
#             )
#         else:
#             return Response(
#                 data=serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )


class BookDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    lookup_field = 'title'
    lookup_url_kwarg = 'target_title'

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BookDetailSerializer
        return BookCreateSerializer

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)

        disc_price = response.data.get('discounted_price')
        price = response.data.get('price')

        if disc_price and price:
            response.data['is_discounted'] = disc_price < price
        else:
            response.data['is_discounted'] = False

        return response



# class BookDetailUpdateDeleteAPIView(APIView):
#     def get(self, request: Request, **kwargs) -> Response:
#         try:
#             book = Book.objects.get(id=kwargs['book_id'])
#         except Book.DoesNotExist:
#             return Response(
#                 data={
#                     "message": "BOOK NOT FOUND"
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )
#
#         serializer = BookDetailSerializer(book)
#
#         return Response(
#             data=serializer.data,
#             status=status.HTTP_200_OK
#         )
#
#     def put(self, request: Request, **kwargs) -> Response:
#         try:
#             book = Book.objects.get(id=kwargs['book_id'])
#         except Book.DoesNotExist:
#             return Response(
#                 data={
#                     "message": "Book not found"
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )
#
#         serializer = BookCreateSerializer(instance=book, data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(
#                 data=serializer.data,
#                 status=status.HTTP_200_OK
#             )
#
#         else:
#             return Response(
#                 data=serializer.errors,
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#
#     def delete(self, request: Request, **kwargs) -> Response:
#         try:
#             book = Book.objects.get(id=kwargs['book_id'])
#         except Book.DoesNotExist:
#             return Response(
#                 data={
#                     "message": "Book not found"
#                 },
#                 status=status.HTTP_404_NOT_FOUND
#             )
#
#         book.delete()
#
#         return Response(
#             data={
#                 "message": "Book was deleted successfully."
#             },
#             status=status.HTTP_204_NO_CONTENT
#         )


# @api_view(['GET', 'POST'])
# def books_list_create(request) -> Response:
#     if request.method == 'GET':
#         books = Book.objects.all()  # Queryset[<Book obj1>, ..., <Book obj150>]
#         serializer = BookListSerializer(books, many=True)
#         return Response(
#             data=serializer.data,
#             status=200
#         )
#     elif request.method == 'POST':
#         serializer = BookCreateSerializer(data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['GET', 'PUT', 'DELETE'])
# def book_detail_update_delete(request, book_id: int) -> Response:
#     if request.method == 'GET':
#         try:
#             book = Book.objects.get(id=book_id)
#         except Book.DoesNotExist:
#             return Response(
#                 data={
#                     "message": "BOOK NOT FOUND"
#                 },
#                 status=404
#             )
#
#         serializer = BookDetailSerializer(book)
#
#         return Response(
#             data=serializer.data,
#             status=200
#         )
#
#     elif request.method == 'PUT':
#         try:
#             book = Book.objects.get(id=book_id)
#         except Book.DoesNotExist:
#             return Response(
#                 data={
#                     "message": "Book not found"
#                 },
#                 status=404
#             )
#
#         serializer = BookCreateSerializer(instance=book, data=request.data)
#
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(
#                 data=serializer.data,
#                 status=200
#             )
#
#         else:
#             return Response(
#                 data=serializer.errors,
#                 status=400
#             )
#     elif request.method == 'DELETE':
#         try:
#             book = Book.objects.get(id=book_id)
#         except Book.DoesNotExist:
#             return Response(
#                 data={
#                     "message": "Book not found"
#                 },
#                 status=404
#             )
#
#         book.delete()
#
#         return Response(
#             data={
#                 "message": "Book was deleted successfully."
#             },
#             status=204
#         )

# @api_view(['POST'])
# def book_create(request):
#     serializer = BookCreateSerializer(data=request.data)
#
#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     else:
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT'])
# def update_book(request, book_id: int) -> Response:
#     try:
#         book = Book.objects.get(id=book_id)
#     except Book.DoesNotExist:
#         return Response(
#             data={
#                 "message": "Book not found"
#             },
#             status=404
#         )
#
#     serializer = BookCreateSerializer(instance=book, data=request.data)
#
#     if serializer.is_valid():
#         serializer.save()
#
#         return Response(
#             data=serializer.data,
#             status=200
#         )
#
#     else:
#         return Response(
#             data=serializer.errors,
#             status=400
#         )


# @api_view(['DELETE'])
# def delete_book(request, book_id: int) -> Response:
#     try:
#         book = Book.objects.get(id=book_id)
#     except Book.DoesNotExist:
#         return Response(
#             data={
#                 "message": "Book not found"
#             },
#             status=404
#         )
#
#     book.delete()
#
#     return Response(
#         data={
#             "message": "Book was deleted successfully."
#         },
#         status=204
#     )
