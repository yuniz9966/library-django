import re
from typing import Any

from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from django.db import transaction

from books.models import Book, User, Author, Genre


class BookSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)
    rating = serializers.FloatField(
        default=0.0,
        min_value=0.0,
        max_value=10.00
    )
    pages = serializers.IntegerField()
    release_year = serializers.DateField()

    class Meta:
        model = None
        fields = ('title', 'rating', 'pages', 'release_year')


class AuthorShortInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = [
            'id',
            'name',
            'surname'
        ]

class BookListSerializer(serializers.ModelSerializer):
    author = AuthorShortInfoSerializer()
    # genre = serializers.StringRelatedField()
    genre = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    class Meta:
        model = Book
        fields = [
            'title',
            'genre',
            'author',
            'publisher',
            'rating',
            'release_year',
            'price'
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        if self.context.get('include_related'):
            representation['publisher'] = {
                "id": instance.publisher.id,
                "username": instance.publisher.username,
                "email": instance.publisher.email,
                "phone": instance.publisher.phone,
                "role": instance.publisher.role,
            }
        else:
            representation.pop('publisher', None)

        return representation


class BookDetailSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField()
    publisher = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all()  # N+1 проблема. в будущем рассмотрим решение
    )

    class Meta:
        model = Book
        fields = "__all__"


class BookCreateSerializer(serializers.ModelSerializer):
    discounted_price = serializers.DecimalField(
        max_digits=6,
        decimal_places=4,
        write_only=True,
        required=False,
        min_value=0
    )

    publisher_email = serializers.EmailField(
        max_length=75,
        required=False
    )


    class Meta:
        model = Book
        fields = [
            'title',
            'rating',
            'genre',
            'release_year',
            'publisher_email',
            'price',
            'discounted_price',
            'pages',
            'language',
            'isbn'
        ]

    # def validate_field_name(self):
    #     ...

    def validate_pages(self, value: int):
        if value < 0:
            raise serializers.ValidationError(
                "The number of pages must be a valid integer and grater than 0"
            )

        return value


    def validate(self, attrs: dict[str, str | int | float]):
        disc_price = attrs.get('discounted_price')

        # if not disc_price:
        #     raise serializers.ValidationError(...)

        if disc_price and disc_price > attrs['price']:
            raise serializers.ValidationError(
                {
                    "discounted_price": "Цена со скидкой НЕ МОЖЕТ быть больше, чем оригинальная цена"
                }
            )

        return attrs

    def create(self, validated_data: dict[str, str | int | float]) -> Book:
        validated_data['discounted_price'] = float(validated_data['price']) * .7
        pub_email = validated_data.pop('publisher_email')
        publisher = User.objects.get(email=pub_email)

        book = Book.objects.create(publisher=publisher, **validated_data)

        return book

        # {
        #     "price": 29.99
        # }
        #
        # -> -> custom_create()
        #
        # {
        #     "price": 29.99,
        #     "disc_price": "price * 0.7"
        # } -> base_create(new_validated_data)


    def update(self, instance: Book, validated_data: dict[str, str | int | float]) -> Book:
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        return instance

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'




class AuthorCreateSerializer(serializers.ModelSerializer):
    books = BookCreateSerializer(many=True, write_only=True)

    class Meta:
        model = Author
        fields = [
            'id',
            'name',
            'surname',
            'books'
        ]

    def create(self, validated_data):
        books_data = validated_data.pop('books')

        with transaction.atomic():
            author = Author.objects.create(**validated_data)

            book_objects = [
                Book(author=author, **book) for book in books_data
            ]

            Book.objects.bulk_create(book_objects)

        return author

    # def create(self, validated_data):
    #     books_data = validated_data.pop('books')
    #
    #     try:
    #         transaction.set_autocommit(False)
    #         author = Author.objects.create(**validated_data)
    #
    #         book_objects = [
    #             Book(author=author, **book) for book in books_data
    #         ]
    #         transaction.commit()
    #
    #         Book.objects.bulk_create(book_objects)
    #     except Exception:
    #         transaction.rollback()
    #
    #     return author
    #
    # def create(self, validated_data):
    #     books_data = validated_data.pop('books')
    #
    #     try:
    #         with transaction.atomic():
    #             author = Author.objects.create(**validated_data)
    #
    #             book_objects = [
    #                 Book(author=author, **book) for book in books_data
    #             ]
    #
    #             if <condition>:
    #                 transaction.set_rollback(True)
    #
    #
    #             transaction.on_commit(lambda: "SUCCESS")
    #
    #             Book.objects.bulk_create(book_objects)
    #     except:
    #         ...
    #
    #     return author




# ======================================================================


# USER REGISTER LOGIC


class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    re_password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(
        choices=[
            ("ADMIN", "ADMIN"),
            ("MODERATOR", "MODERATOR"),
            ("LIB MEMBER", "LIB MEMBER"),
        ],
        required=False
    )
    is_staff = serializers.BooleanField(required=False)

    class Meta:
        model = User
        fields = [
            'username', 'first_name',
            'last_name', 'password',
            're_password', 'email',
            'role', 'is_staff',
        ]

    def validate(self, attrs):
        first_name = attrs.get('first_name')
        last_name = attrs.get('last_name')

        re_pattern = r'^[a-zA-Z]+$'

        if not re.match(re_pattern, first_name):
            raise serializers.ValidationError(
                {"first_name": "First name must contain only alphabet characters."}
            )

        if not re.match(re_pattern, last_name):
            raise serializers.ValidationError(
                {"last_name": "Last name must contain only alphabet characters."}
            )

        password = attrs.get('password')
        re_password = attrs.pop('re_password', None)

        if not password:
            raise serializers.ValidationError(
                {"password": "This field is Required."}
            )

        if not re_password:
            raise serializers.ValidationError(
                {"re_password": "This field is Required."}
            )

        validate_password(password)

        if password != re_password:
            raise serializers.ValidationError(
                {"re_password": "Password didn't match."}
            )

        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)

        user.save()

        return user
