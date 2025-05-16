import datetime

from django.contrib.auth import authenticate
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoModelPermissions, AllowAny
from django.db.models import Count
from django.utils import timezone
from rest_framework.permissions import SAFE_METHODS
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status, filters
from rest_framework.generics import (
    ListAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from django.db import transaction
from rest_framework_simplejwt.tokens import RefreshToken

from books.debug_tools import QueryDebug
from books.models import Genre, Author
from books.permissions.owner_permissions import IsBookOwnerOrReadOnly
from books.permissions.statistic_model_permissions import CanGetStatisticPermission
from books.serializers import (
    GenreSerializer,
    AuthorCreateSerializer,
    AuthorShortInfoSerializer
)
from books.serializers import (
    BookListSerializer,
    BookDetailSerializer,
    BookCreateSerializer
)
from books.models import Book


class UserBooksListGenericView(ListAPIView):
    serializer_class = BookListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Book.objects.filter(
            publisher=self.request.user
        )


class GenreViewSet(ModelViewSet):
    queryset = Genre.objects.all()  # SELECT * FROM genres; -> SELECT * FROM genres WHERE id IN (1, 7, 19)
    serializer_class = GenreSerializer
    # permission_classes = [
    #     DjangoModelPermissions,
    #     CanGetStatisticPermission
    # ]

    def get_permissions(self):
        if self.action == 'get_books_count_by_genre':
            return [CanGetStatisticPermission()]
        return [DjangoModelPermissions()]

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


class AuthorCreateView(CreateAPIView):
    serializer_class = AuthorCreateSerializer
    queryset = Author.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return AuthorShortInfoSerializer
        return AuthorCreateSerializer

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        if 'surname' not in data or not data['surname']:
            data['surname'] = 'UNKNOWN'

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )


class BooksByRegularIsbn(ListAPIView):
    serializer_class = BookListSerializer

    def get_queryset(self):
        queryset = Book.objects.filter(
            isbn=self.kwargs.get("isbn")
        )
        return queryset


class GetBook(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookDetailSerializer
    lookup_field = 'title'
    lookup_url_kwarg = 'book_title'

class BooksListCreateView(ListCreateAPIView):
    queryset = Book.objects.select_related(
        'author', 'publisher'
    ).all()
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

    @QueryDebug(file_name='book_all.log')
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data.copy()

        if 'title' not in data or not data['title']:
            data['title'] = 'UNKNOWN TITLE'

        if 'release_year' not in data or not data['release_year']:
            data['release_year'] = timezone.now()

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED
        )


class BookDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    permission_classes = [IsBookOwnerOrReadOnly]
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



# ===================================================================================================
# ===================================================================================================
# ===================================================================================================

# User JWT Logic




class LogInAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request: Request) -> Response:
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(
            request=request,
            username=username,
            password=password
        )

        if user:
            refresh_token = RefreshToken.for_user(user)
            access_token = refresh_token.access_token

            access_expiry = datetime.datetime.fromtimestamp(access_token['exp'], datetime.UTC)
            refresh_expiry = datetime.datetime.fromtimestamp(refresh_token['exp'], datetime.UTC)

            response = Response(status=status.HTTP_200_OK)

            response.set_cookie(
                key='access_token',
                value=str(access_token),
                httponly=True,
                secure=False,
                samesite='Lax',
                expires=access_expiry
            )

            response.set_cookie(
                key='refresh_token',
                value=str(refresh_token),
                httponly=True,
                secure=False,
                samesite='Lax',
                expires=refresh_expiry
            )

            return response

        else:
            return Response(
                data={"message": "Invalid username or password."},
                status=status.HTTP_401_UNAUTHORIZED
            )


class LogOutAPIView(APIView):
    def post(self, request):
        response = Response(status=status.HTTP_200_OK)

        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')

        return response
