from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.title, name="title"),
    path("error", views.error, name="error")
    #path("newentry", views.newEntry, name="newentry")
]
