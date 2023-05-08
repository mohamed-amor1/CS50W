# Import necessary modules and classes from Django
from django.urls import path
from . import views

# Define the namespace for the tasks app
app_name = "tasks"

# Define the URL patterns for the tasks app
urlpatterns = [
    path("", views.index, name="index"),  # Maps the root URL to the index view
    path("add", views.add, name="add"),  # Maps the "/add" URL to the add view
]
