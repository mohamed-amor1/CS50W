# Import necessary modules
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.template import TemplateDoesNotExist
from .forms import NewPageForm, EditPageForm
from . import util
import os
import markdown2
import random


# Define the views for the encyclopedia app
def index(request):
    # Render the index.html template and pass the entries list to it
    return render(request, "encyclopedia/index.html", {"entries": util.list_entries()})


def entry(request, title):
    try:
        # Check if the markdown file for the given title exists
        md_file_path = os.path.join("entries", f"{title}.md")
        if os.path.exists(md_file_path):
            # If the file exists, read the contents, convert to HTML, and render the entry.html template with the HTML content
            with open(md_file_path, "r") as file:
                markdown_text = file.read()
                html = markdown2.markdown(markdown_text)
                return render(
                    request,
                    "encyclopedia/entry.html",
                    {"title": title, "html_content": html},
                )
        else:
            # If the file doesn't exist, return a 404 error
            return HttpResponseNotFound("404: Page not found")
    except TemplateDoesNotExist:
        # Handle the case when the template doesn't exist
        return HttpResponseNotFound("404: Page not found")


def random_entry(request):
    # Pick a random entry from the list of entries and redirect to its entry page
    entries_list = util.list_entries()
    random_entry = random.choice(entries_list)
    return redirect("entry", title=random_entry)


def search_entry(request):
    if request.method == "POST":
        # Get the search query from the form data
        q = request.POST.get("q")
        matching_entries = []
        entries_list = util.list_entries()
        for entry_x in entries_list:
            # Check if the query exactly matches an entry title
            if q == entry_x.lower():
                return redirect("entry", title=q)
            # Check if the query is a substring of an entry title
            elif q in entry_x.lower():
                matching_entries.append(entry_x)
        if matching_entries:
            # If there are matching entries, render the search_results.html template with the list of entries
            return render(
                request,
                "encyclopedia/search_results.html",
                {"entries": matching_entries},
            )
        else:
            # If there are no matching entries, render the search_results.html template with no entries
            return render(request, "encyclopedia/search_results.html")
    # Handle the case when the request method is not POST
    return HttpResponse("Invalid request method.")


def new_page(request):
    if request.method == "POST":
        # If the form is submitted, validate the form data and save the new entry to the entries directory
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if util.get_entry(title):
                # If the entry already exists, return an error
                return HttpResponse("Error: entry already exists.")
            util.save_entry(title, content)
            return redirect("entry", title=title)
    else:
        # If the form is not submitted, render the new_page.html template with an empty form
        form = NewPageForm()
    return render(request, "encyclopedia/new_page.html", {"form": form})


def edit_page(request, title):
    if request.method == "POST":
        # If the form is submitted via POST method
        form = EditPageForm(request.POST)
        if form.is_valid():
            # Validate the form data
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")
            if util.get_entry(title):
                # If the entry already exists, update its content
                util.save_entry(title, content)
            return redirect("entry", title=title)
    elif title:
        # If the form is not submitted and a title is provided in the URL
        md_file_path = os.path.join("entries", f"{title}.md")
        if os.path.exists(md_file_path):
            # If the markdown file for the title exists, prepopulate the form with its content
            with open(md_file_path, "r") as file:
                markdown_text = file.read()
                form = EditPageForm(initial={"title": title, "content": markdown_text})
        else:
            form = EditPageForm()
            # Handle the case when the file doesn't exist
    else:
        # If the form is not submitted and no title is provided in the URL
        form = EditPageForm()

    return render(request, "encyclopedia/edit_page.html", {"form": form})
