from rest_framework import serializers

from books.models import Book


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


class BookListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'title',
            'genre',
            'author',
            'rating',
            'release_year',
            'price'
        ]


class BookDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = "__all__"


class BookCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = [
            'title',
            'rating',
            'genre',
            'release_year',
            'author',
            'price',
            'pages',
            'language',
            'isbn'
        ]
