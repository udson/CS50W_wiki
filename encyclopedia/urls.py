from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("?q=<str:q>", views.entry, name="search"),
    path("wiki/<str:entry_title>", views.entry, name="entry"),
]
