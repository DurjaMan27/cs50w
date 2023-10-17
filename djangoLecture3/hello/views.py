from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    #return HttpResponse("Hello!")
    return render(request, "hello/index.html")

def varun(request):
    return HttpResponse("Hello, Varun!")

def greet(request, name):
    # return HttpResponse(f"Hello, {name.capitalize()}!")
    return render(request, "hello/greet.html", {
        "name": name.capitalize() # gives HTML file access to a variable that represents name.capitalize()
    })