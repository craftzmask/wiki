import random
import markdown2

from django.shortcuts import render
from django.http import Http404, HttpResponseRedirect, HttpResponseBadRequest
from django.urls import reverse
from django import forms

from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label='Title', max_length=50)
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": 10, "cols": 50}))

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
        'entry': markdown2.markdown(entry)
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


def create(request):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            
            if util.get_entry(title):
                return HttpResponseBadRequest('<h1>The entry is already existed</h1>')
            
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse('encyclopedia:index'))
        else:
            return render(request, 'encyclopedia/create.html', {
                'form': form
            })
            
    return render(request, 'encyclopedia/create.html', {
        'form': NewEntryForm()
    })
    
    
def edit(request, title):
    if request.method == 'POST':
        form = NewEntryForm(request.POST)
        print(form)
        if form.is_valid():
            content = form.cleaned_data['content']
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse(
                'encyclopedia:view_entry', args=[title]
            ))
        else:
            return render(request, 'encyclopedia/edit.html', {
                'title': title,
                'form': form
            })
    
    form = NewEntryForm(initial={
        'title': title,
        'content': util.get_entry(title)
    })
    
    # Ensure the title cannot be changed
    form.fields['title'].widget.attrs['readonly'] = True

    return render(request, 'encyclopedia/edit.html', {
        'title': title,
        'form': form
    })
    
    
def random_entry(request):
    return HttpResponseRedirect(reverse(
        'encyclopedia:view_entry',
        args=[random.choice(util.list_entries())]
    ))