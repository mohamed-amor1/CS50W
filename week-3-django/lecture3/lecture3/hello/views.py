from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "hello/index.html")


def mohamed(request):
    return HttpResponse("Hello, Mohamed!")


def yassine(request):
    return HttpResponse("Hello, Yassine!")


def greet(request, name):
    return render(request, "hello/greet.html", {"name": name.capitalize()})
