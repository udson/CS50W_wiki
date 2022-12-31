from markdown2 import markdown
from random import choice

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

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


def search(request):
    found = [item for item in util.list_entries() if request.GET['q'] in item]
    if len(found):
        if request.GET['q'] not in found:
            return render(request, "encyclopedia/search_results.html", {
                "q": request.GET['q'],
                "entries": found,
            })
    return HttpResponseRedirect(reverse('entry', args=[request.GET['q']]))


def random_entry(request):
    return HttpResponseRedirect(reverse('entry', args=[choice(util.list_entries())]))
