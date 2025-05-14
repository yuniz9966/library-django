"""
URL configuration for library project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter, SimpleRouter

from books.views import (
    # BooksListCreateAPIView,
    BooksListCreateView,
    # BookDetailUpdateDeleteAPIView,
    BookDetailUpdateDeleteView,
    GenreViewSet,
    BooksByRegularIsbn, AuthorCreateView,GetBook
)

router = DefaultRouter()

router.register(r'genres', GenreViewSet)


# http://127.0.0.1:8000/admin/
urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', BooksListCreateView.as_view()),
    path('books/<str:target_title>/', BookDetailUpdateDeleteView.as_view()),
    re_path(
        r'^books-isbn/(?P<isbn>\d{3}-\d{1,5}-\d{1,7}-\d{1,7}-\d)/?$',
        BooksByRegularIsbn.as_view()
    ),
    path('author-create/', AuthorCreateView.as_view()),
    path('get-book/<str:book_title>/', GetBook.as_view()),
    path('auth-login/', obtain_auth_token),
    path('auth-login-jwt/', TokenObtainPairView.as_view()),
    path('token-refresh/', TokenRefreshView.as_view()),
] + router.urls

# isbn = 3-1,5-1,7-1,7-1