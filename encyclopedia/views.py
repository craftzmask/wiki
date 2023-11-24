from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

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
    

def search(request):
    query = request.GET['q']
    
    titles = util.list_entries()
    
    if titles.count(query) == 1:
        return HttpResponseRedirect(reverse(
            'encyclopedia:view_entry', args=[query]
        ))
    
    search_result = [title for title in titles if query in title]
    return render(request, 'encyclopedia/index.html', {
        'entries': search_result
    })

    