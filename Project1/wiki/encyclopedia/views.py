from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random
import markdown
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


from . import util

class NewTaskForm(forms.Form):
    title = forms.CharField(label="Wiki Page Title", max_length=20, )
    content = forms.CharField(label="content", widget=forms.Textarea(), max_length=400)

class EditTaskForm(forms.Form):
    content = forms.CharField(label="content", widget=forms.Textarea(), max_length=400)

    def __init__(self, *args, **kwargs):
        title = kwargs.pop('title', '')  # Get the 'title' argument passed when creating the form
        super(EditTaskForm, self).__init__(*args, **kwargs)

        # Set the initial value of 'content' based on the title
        if title:
            page_content = util.get_entry(title)
            if page_content:
                self.fields['content'].initial = page_content

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    returnVal = render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": util.get_entry(title)
    })

    if util.get_entry(title) == None:
        '''return render(request, "encyclopedia/error.html", {
            "title": title.capitalize()
        })'''
        return HttpResponseRedirect(reverse("error"))
    else:
        return returnVal

def searchError(request):
    return render(request, "encyclopedia/searchError.html")


def newEntry(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            if util.get_entry(form.cleaned_data["title"]) != None:
                print("i am here...")
                return render(request, "encyclopedia/newEntryError.html", {
                    "title": form.cleaned_data["title"]
                })
            else:
                util.save_entry(form.cleaned_data["title"], form.cleaned_data["content"])
                return HttpResponseRedirect(reverse("title", kwargs={'title': form.cleaned_data["title"]}))
        else:
            return render(request, "encyclopedia/newentry.html", {
                "form": form
            })

    return render(request, "encyclopedia/newentry.html", {
        "form": NewTaskForm()
    })

def editEntry(request, title):
    if request.method == "POST":
        form = EditTaskForm(request.POST, title=title)
        if form.is_valid():
            util.save_entry(title, form.cleaned_data["content"])
            return HttpResponseRedirect(reverse("title", kwargs={'title': title}))
        else:
            return render(request, "encyclopedia/editentry.html", {
                "form": form,
                "title": title
            })

    return render(request, "encyclopedia/editentry.html", {
        "form": EditTaskForm(title=title),
        "title": title
    })

def randomPage(request):
    list_entries = util.list_entries()

    return title(request, random.choice(list_entries))