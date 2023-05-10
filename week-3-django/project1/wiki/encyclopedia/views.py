from django.shortcuts import render
import os
import markdown2
from django.shortcuts import redirect
from django.http import HttpResponseNotFound
from django.template import TemplateDoesNotExist
import random
from django.http import HttpResponse
from .forms import NewPageForm, EditPageForm


from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, title):
    try:
        md_file_path = os.path.join("entries", f"{title}.md")

        if os.path.exists(md_file_path):
            with open(md_file_path, "r") as file:
                markdown_text = file.read()
                html = markdown2.markdown(markdown_text)
                return render(
                    request,
                    "encyclopedia/entry.html",
                    {"title": title, "html_content": html},
                )
        else:
            return HttpResponseNotFound("404: Page not found")
    except TemplateDoesNotExist:
        return HttpResponseNotFound("404: Page not found")


def random_entry(request):
    entries_list = util.list_entries()
    random_entry = random.choice(entries_list)
    return redirect("entry", title=random_entry)


def search_entry(request):
    if request.method == "POST":
        q = request.POST.get("q")
        matching_entries = []
        entries_list = util.list_entries()
        for entry_x in entries_list:
            if q == entry_x.lower():
                return redirect("entry", title=q)
            elif q in entry_x.lower():
                matching_entries.append(entry_x)

        if matching_entries:
            return render(
                request,
                "encyclopedia/search_results.html",
                {"entries": matching_entries},
            )
        else:
            return render(request, "encyclopedia/search_results.html")

    return HttpResponse("Invalid request method.")


def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title):
                return HttpResponse("Error: entry already exists.")
            util.save_entry(title, content)
            return redirect("entry", title=title)

    else:
        form = NewPageForm()
    return render(request, "encyclopedia/new_page.html", {"form": form})


def edit_page(request, title):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")
            if util.get_entry(title):
                util.save_entry(title, content)
            return redirect("entry", title=title)
    elif title:
        md_file_path = os.path.join("entries", f"{title}.md")
        if os.path.exists(md_file_path):
            with open(md_file_path, "r") as file:
                markdown_text = file.read()
                form = EditPageForm(initial={"title": title, "content": markdown_text})
        else:
            form = EditPageForm()
            # Handle the case when the file doesn't exist
    else:
        # Handle the case when the title is not available in the URL
        form = EditPageForm()

    return render(request, "encyclopedia/edit_page.html", {"form": form})
