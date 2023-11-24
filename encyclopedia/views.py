from django.http import Http404
from django.shortcuts import render

from . import util

# Create your views here.
def index(request):
    return render(request, 'encyclopedia/index.html', {
        'entries': util.list_entries()
    })


def view_entry(request, title):
    entry = util.get_entry(title)
    if not entry:
        raise Http404("Entry does not exist")
    return render(request, 'encyclopedia/entry.html', {
        'title': title,
        'entry': entry
    })