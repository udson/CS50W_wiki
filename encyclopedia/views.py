from markdown2 import markdown
from random import choice

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from . import util
from .forms import *


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


def new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            if util.get_entry(title) is None:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse(
                    'entry', args=[request.POST['title']]
                ))
            form.add_error(field=None, error=f'Error! The entry "{title}" already exists.')
    else:
        form = NewEntryForm()

    return render(request, "encyclopedia/new_entry.html", {
        "form": form,
    })


def edit_entry(request, entry_title):
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            content = f"{form.cleaned_data['content']}\n"
            util.save_entry(entry_title, content)
            return HttpResponseRedirect(reverse(
                'entry', args=[entry_title]
            ))
    else:
        form = EditEntryForm({
            "content": util.get_entry(entry_title),
        })

    return render(request, "encyclopedia/edit_entry.html", {
        "title": entry_title,
        "form": form,
    }) 