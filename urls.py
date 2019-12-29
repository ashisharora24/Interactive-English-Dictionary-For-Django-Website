# this is for testing only
from django.contrib import admin
from django.urls import path

from .views import (
    home_page,
    confirmed_words_to_meaning
)

urlpatterns = [
    path('', home_page),
    path('word/<str:word>/', confirmed_words_to_meaning),
]
