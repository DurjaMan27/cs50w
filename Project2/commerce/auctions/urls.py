from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.newlisting, name="newlisting"),
    path("categories", views.categories, name="categories"),
    path("listings/<str:category>", views.all_listings, name="all_listings"),
    path("closeAuction", views.close_auction, name="close_auction"),
    path("<str:username>/<str:product>", views.listing, name="listing"),
    path("error", views.error, name="error"),
    path("addToWatchList", views.addWatchList, name="addWatchList"),
    path("watchlist", views.watchlist, name="watchlist")
]
