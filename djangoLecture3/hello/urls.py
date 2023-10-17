from django.urls import path
from . import views # imports the views file from the same directory

urlpatterns = [
    path("", views.index, name="index"), # once this default path is taken, the index file will be run
    path("varun", views.varun, name="varun"), # accessed by /hello/varun
    path("<str:name>", views.greet, name="greet") # allows for any string name
]