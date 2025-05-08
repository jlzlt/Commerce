from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listings/<int:id>", views.listing, name="listing"),
    path("listings/<int:id>/watchlist", views.toggle_watchlist, name="toggle_watchlist"),
    path("listing/<int:id>/close", views.close_auction, name="close_auction"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
]
