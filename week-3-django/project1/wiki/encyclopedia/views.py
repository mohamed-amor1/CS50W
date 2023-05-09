from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.template import TemplateDoesNotExist
from django.shortcuts import redirect
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, title):
    try:
        return render(
            request, f"encyclopedia/{title}.html", {"title": util.get_entry(title)}
        )
    except TemplateDoesNotExist:
        return HttpResponseNotFound("404: Page not found")


def random_entry(request):
    entries_list = util.list_entries()
    random_entry = random.choice(entries_list)
    return redirect("entry", title=random_entry)
