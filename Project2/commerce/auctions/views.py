from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Comment, Bid

class NewListingForm(forms.Form):
    CATEGORY_CHOICES = [
        ('General', 'General'),
        ('Home', 'Home'),
        ('Fashion', 'Fashion'),
        ('Toys', 'Toys'),
        ('Electronics', 'Electronics')
    ]
    title = forms.CharField(label="Product", widget=forms.TextInput(attrs={'placeholder': 'Product Title'}))
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'placeholder':'Product Description'}))
    startingBid = forms.IntegerField(label="Starting Bid")
    productCategory = forms.ChoiceField(label="category", choices=CATEGORY_CHOICES)
    productImage = forms.URLField(label="image", required=False)

def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        'listings': listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


def createListing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            newListing = Listing.objects.create(poster=request.user, title=form.cleaned_data["title"],
                                    description=form.cleaned_data["description"],
                                    startingBid=form.cleaned_data["startingBid"],
                                    category=form.cleaned_data["productCategory"],
                                    image=form.cleaned_data["productImage"])
            #print(newListing)
            return HttpResponseRedirect(reverse("listing", kwargs={'username': request.user, 'listingID': newListing.listingID}))
        else:
            return render(request, "auctions/createListing.html", {
                "form": NewListingForm()
            })
    else:
        return render(request, "auctions/createListing.html", {
            "form": NewListingForm()
        })

def listing(request, username, listingID):
    listing = Listing.objects.get(pk=listingID)