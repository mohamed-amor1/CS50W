from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>/", views.entry, name="entry"),
    path("random/", views.random_entry, name="random_entry"),
    path("search_entry/", views.search_entry, name="search_entry"),
    path("new_page/", views.new_page, name="new_page"),
    path("wiki/edit/<str:title>/", views.edit_page, name="edit_page"),
]
