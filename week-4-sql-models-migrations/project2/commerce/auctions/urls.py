from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create_listing", views.create_listing, name="create_listing"),
    path("listing_page/<int:id>", views.listing_page, name="listing_page"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("user/<int:seller_id>", views.user, name="user"),
    path("categories", views.categories, name="categories"),
    path("categories/<slug:category>/", views.category_page, name="category_page"),
]
