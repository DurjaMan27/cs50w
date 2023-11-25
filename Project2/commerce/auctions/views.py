from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Comment, Bid

class NewListingForm(forms.Form):
    title = forms.CharField(label="Product", widget=forms.TextInput(attrs={'placeholder': 'Product Title'}))
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'placeholder':'Product Description'}))
    startingBid = forms.IntegerField(label="Starting Bid")
    productCategory = forms.CharField(label="category", required=False)
    productImage = forms.URLField(label="image", required=False)

class NewCommentForm(forms.Form):
    comment = forms.CharField(label="Comment", max_length=500)

class NewBidForm(forms.Form):
    bid_amount = forms.IntegerField(label="Bid")


def index(request):
    return render(request, "auctions/index.html")


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

def newlisting(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            #models.newObject
            print("hello")
        else:
            return render(request, "commerce/create.html", {
                "form": form
            })

    return render(request, "commerce/create.html", {
        "form": NewListingForm()
    })

def listing(request, username, product):
    listing = Listing.objects.get(product=product, user=username)
    comments = Comment.objects.get(product=product, product_poster=username)
    bids = Bid.objects.get(product=product, product_poster=username)
    if request.method == "POST":
        bidForm = NewBidForm(request.POST, username=username, product=product)
        commentForm = NewCommentForm(request.POST, username=username, product=product)
        if 'bidSubmit' in request.POST:
            if bidForm.is_valid():
                bid = Bid.objects.get(user=username)

                # Finding the bidAmount from the submitted form data
                newBidAmount = int(request.POST["bid_amount"])

                if newBidAmount <= listing.product_startingBid:
                    return HttpResponse("Your bid is too low. Please enter a bid amount that is greater than the current bid.")
                else:
                    # Finding the passenger based on the id
                    user = request.User

                    # Add passenger to the flight
                    bid.user = user
                    bid.bid_amount = newBidAmount
                    listing.product_startingBid = newBidAmount
                    listing.product_description = user

                    # Reload page
                    return render(request, "auctions/listing.html", {
                        "listing": listing,
                        "comments": comments,
                        "bids": bids,
                        "bid_form": NewBidForm(),
                        "comment_form": NewCommentForm()
                    })
        elif 'commentSubmit' in request.POST:
            if commentForm.is_valid():
                # Finding the bidAmount from the submitted form data
                newComment = int(request.POST["comment"])

                # Finding the passenger based on the id
                user = request.User

                # Add passenger to the flight
                listing.product_startingBid = newBidAmount
                listing.product_description = user

                # Reload page
                return render(request, "auctions/listing.html", {
                    "listing": listing,
                    "comments": comments,
                    "bids": bids,
                    "bid_form": NewBidForm(),
                    "comment_form": NewCommentForm()
                })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "comments": comments,
            "bids": bids,
            "bid_form": NewBidForm(),
            "comment_form": NewCommentForm()
        })