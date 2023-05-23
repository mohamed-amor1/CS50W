from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path(
        "user-profile/<str:username>/json/",
        views.user_profile_json,
        name="user_profile_json",
    ),
    path("follow/", views.follow_user, name="follow_user"),
]
