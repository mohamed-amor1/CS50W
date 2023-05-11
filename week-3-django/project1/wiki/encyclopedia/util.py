import re
import random
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.shortcuts import redirect


def list_entries():
    """
    Returns a list of all names of encyclopedia entries.
    """
    # Get the list of filenames in the 'entries' directory
    _, filenames = default_storage.listdir("entries")

    # Filter the filenames to include only those ending with '.md'
    entries = [
        re.sub(r"\.md$", "", filename)
        for filename in filenames
        if filename.endswith(".md")
    ]

    # Sort the entries alphabetically
    entries.sort()

    return entries


def save_entry(title, content):
    """
    Saves an encyclopedia entry, given its title and Markdown content.
    If an existing entry with the same title already exists, it is replaced.
    """
    filename = f"entries/{title}.md"

    # Delete the existing entry if it exists
    if default_storage.exists(filename):
        default_storage.delete(filename)

    # Save the new entry
    default_storage.save(filename, ContentFile(content))


def get_entry(title):
    """
    Retrieves an encyclopedia entry by its title.
    If no such entry exists, the function returns None.
    """
    try:
        # Open the file for reading
        f = default_storage.open(f"entries/{title}.md")

        # Read the contents of the file
        entry_content = f.read().decode("utf-8")

        # Close the file
        f.close()

        return entry_content
    except FileNotFoundError:
        return None
