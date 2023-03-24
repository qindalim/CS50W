from hashlib import new
from django.http.response import HttpResponse
from encyclopedia import urls
from django.shortcuts import get_object_or_404, render
from django import forms
from django.http import HttpResponseNotFound

from . import util

import markdown
import random

class NewPageForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={"placeholder": "Title"}))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={"placeholder": "Content"}))

class EditForm(forms.Form):
    content = forms.CharField(label="", widget=forms.Textarea())

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def entry(request, name):
    if util.get_entry(name):
        return render(request, "encyclopedia/entry.html", {
            "title": name,
            "content": markdown.markdown(util.get_entry(name))
        })
    else: 
        return HttpResponseNotFound("<h1>Page not found</h1>")

def search(request):
    if request.method == "GET":
        task = request.GET.get("q")
        if util.get_entry(task):
            return render(request, "encyclopedia/entry.html", {
                "title": task,
                "content": markdown.markdown(util.get_entry(task))
                })
        elif [entry for entry in util.list_entries() if task in entry.lower()]:
            return render(request, "encyclopedia/search.html", {
                "entries": [entry for entry in util.list_entries() if task in entry.lower()]
                })
        else:
            return render(request, "encyclopedia/searcherror.html", {
                "entries": util.list_entries(),
                })

def newpage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            newtitle = form.cleaned_data["title"]
            newcontent = form.cleaned_data["content"]
            if util.add_entry(newtitle, newcontent): 
                return render(request, "encyclopedia/entry.html", {
                        "title": newtitle,
                        "content": markdown.markdown(util.get_entry(newtitle))
                        })
            else: 
                return render(request, "encyclopedia/newpageerror.html")
        else:
            return render(request, "encyclopedia/newpage.html", {
                "form": form
            })
    return render(request, "encyclopedia/newpage.html", {
        "form": NewPageForm()
    })

def editpage(request, name):
    if request.method == "GET":
        entry = util.get_entry(name)
        return render(request, "encyclopedia/editpage.html", {
                    "title": name,
                    "edit": EditForm(initial={"content": util.get_entry(name)})
                    })
    else:
        form = EditForm(request.POST)
        if form.is_valid():
            newcontent = form.cleaned_data["content"]
            util.save_entry(name, newcontent)
            return render(request, "encyclopedia/entry.html", {
                    "title": name,
                    "content": markdown.markdown(util.get_entry(name))
                    })

def randompage(request):
    entries = util.list_entries()
    name = random.choice(entries)
    return entry(request, name)