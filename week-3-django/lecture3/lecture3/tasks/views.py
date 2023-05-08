from django import forms
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse


# Define a form for creating new tasks
class NewTaskForm(forms.Form):
    task = forms.CharField(label="New Task")


# View function for the index page
def index(request):
    # Check if "tasks" key exists in session
    if "tasks" not in request.session:
        # If not, initialize an empty list for tasks
        request.session["tasks"] = []
    # Render the index.html template with the tasks data from session
    return render(request, "tasks/index.html", {"tasks": request.session["tasks"]})


# View function for adding a new task
def add(request):
    # Check if the request method is POST (form submission)
    if request.method == "POST":
        # Create a form instance with the POST data
        form = NewTaskForm(request.POST)
        # Check if the form data is valid
        if form.is_valid():
            # Extract the task from the form's cleaned data
            task = form.cleaned_data["task"]
            # Append the task to the tasks list in session
            request.session["tasks"] += [task]
            # Redirect the user to the index page
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            # If the form is not valid, render the add.html template with the form data
            return render(request, "tasks/add.html", {"form": form})
    # If the request method is not POST, create a new form instance
    # and render the add.html template with the form data
    return render(request, "tasks/add.html", {"form": NewTaskForm()})
