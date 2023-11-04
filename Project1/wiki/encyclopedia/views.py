from django.shortcuts import render
from django import forms
from django.urls import reverse
from django.http import HttpResponseRedirect


from . import util

class NewTaskForm(forms.Form):
    title = forms.CharField(label="Wiki Page Title", max_length=20)
    content = forms.CharField(label="content", widget=forms.Textarea(), max_length=400)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    returnVal = render(request, "encyclopedia/entry.html", {
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
        #variableTitle = form.cleaned_data["title"]
        #variableTitle = form.title
        #print("this is title ", variableTitle)
        if form.is_valid():
            #task = form.cleaned_data["task"]
            #request.session["tasks"] += [task]
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