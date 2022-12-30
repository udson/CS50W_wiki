from markdown2 import markdown

from django.shortcuts import render

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry_title):
    content = util.get_entry(entry_title)

    if content is None:
        return entry_not_found(request, entry_title)
    
    return render(request, "encyclopedia/entry.html", {
        "title": entry_title,
        "content": markdown(content)
    })


def entry_not_found(request, entry_title):
    return render(request, "encyclopedia/entry_not_found.html", {
        "title": entry_title
    })
