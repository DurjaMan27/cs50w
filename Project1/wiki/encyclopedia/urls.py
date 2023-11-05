from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("searchError", views.searchError, name="searchError"),
    path("newentry", views.newEntry, name="newentry"),
    path("editentry/<str:title>", views.editEntry, name="editentry"),
    path("randompage", views.randomPage, name="randompage"),
    path("search", views.search, name="search")
]
