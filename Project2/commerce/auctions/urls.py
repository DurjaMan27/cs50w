from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("error/<int:listingID>", views.error, name="error"),
    path("createListing", views.createListing, name="createListing"),
    path("categories", views.category, name="category"),
    path("categories/<str:category>", views.categorySpecific, name="categorySpecific"),
    path("listing/<str:username>/<int:listingID>", views.listing, name="listing"),
    path("addWatchList/<int:listingID>", views.addWatchList, name="addWatchList"),
    path("watchlist", views.watchList, name="watchlist"),
    path("closeListing", views.closeListing, name="closeListing")
]
