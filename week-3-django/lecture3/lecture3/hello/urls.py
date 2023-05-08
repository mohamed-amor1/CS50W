from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:name>", views.greet, name="greet"),
    path("mohamed", views.mohamed, name="mohamed"),
    path("yassine", views.yassine, name="yassine"),
]
