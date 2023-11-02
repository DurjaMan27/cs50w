from django.shortcuts import render
from django import forms


from . import util

class NewTaskForm(forms.Form):
    title = forms.CharField(label="newEntry")
    content = forms.Textarea(label="content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    returnVal = render(request, f"encyclopedia/{title}.html", {
        "title": util.get_entry(title)
    })

    if returnVal == None:
        return render(request, "encyclopedia/error.html", {
            "title": title.capitalize()
        })
    else:
        return returnVal

def newEntry(request):
    if request.method == "POST":
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task = form.cleaned_data["task"]
            request.session["tasks"] += [task]
            return HttpResponseRedirect(reverse("tasks:index"))
        else:
            return render(request, "encyclopedia/add.html", {
                "form": form
            })

    return render(request, "encyclopedia/add.html", {
        "form": NewTaskForm()
    })