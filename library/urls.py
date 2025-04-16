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
from django.urls import path

from books.views import list_of_books, get_book_detail, book_create, update_book, delete_book

# http://127.0.0.1:8000/admin/
urlpatterns = [
    path('admin/', admin.site.urls),
    path('books/', list_of_books),
    path('books/<int:book_id>/', get_book_detail),
    path('books/<int:book_id>/update/', update_book),
    path('books/<int:book_id>/delete/', delete_book),
    path('books/create/', book_create),
]
