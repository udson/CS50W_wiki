from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("random", views.random_entry, name="random"),
    path("search", views.search, name="search"),
    path("wiki/new_entry", views.new_entry, name="new_entry"),
    path("wiki/<str:entry_title>", views.entry, name="entry"),
]
