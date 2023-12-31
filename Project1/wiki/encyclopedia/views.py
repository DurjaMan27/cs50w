from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect
import random
from markdown2 import markdown
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage


from . import util

class NewTaskForm(forms.Form):
    #title = forms.CharField(label="title", max_length=40)
    #content = forms.CharField(label="Wiki Page Content", widget=forms.Textarea(), max_length=400)
    title = forms.CharField(label="Title", widget=forms.TextInput(attrs={'placeholder': 'Wiki Page Title', 'style': 'width: 350px; height: 25px;'}))
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'placeholder':'Page Content', 'style': 'width: 600px; display: grid;'}))


class EditTaskForm(forms.Form):
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={'placeholder':'Page Content', 'style': 'width: 600px; display: grid;'}))
    #content = forms.CharField(label="content", widget=forms.Textarea(), max_length=400)

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
    content = util.get_entry(title)
    if util.get_entry(title) == None:
        return HttpResponseRedirect(reverse("searchError"))
    else:
        #return returnVal
        returnVal = markdown(content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "content": returnVal
            })

def searchError(request):
    return render(request, "encyclopedia/searchError.html")

def search(request):
    q = request.GET.get('q').strip()
    listval = [x.lower() for x in util.list_entries()]
    if q.lower() in listval:
        return HttpResponseRedirect(reverse("title", kwargs={'title': q}))
    elif len(util.search(q)) == 0:
        return HttpResponseRedirect(reverse("searchError"))
    else:
        return render(request, "encyclopedia/searchresults.html", {
            "entries": util.search(q),
            "q": q
            })


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