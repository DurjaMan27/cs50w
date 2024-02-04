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
    amount = forms.IntegerField(label="Starting Bid")
    productCategory = forms.ChoiceField(label="category", choices=CATEGORY_CHOICES)
    productImage = forms.URLField(label="image", required=False)

class NewCommentForm(forms.Form):
    comment = forms.CharField(label="Comment", widget=forms.TextInput(attrs={'placeholder': 'Comment Here'}))

class NewBidForm(forms.Form):
    bid = forms.IntegerField(label="Bid")

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

def error(request, listingID):
    listing = Listing.objects.get(pk=listingID)
    return render(request, "auctions/error.html", {
        'listing': listing,
        'otherUser': listing.poster
    })

def createListing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            newListing = Listing.objects.create(poster=request.user, title=form.cleaned_data["title"],
                                    currentPrice=form.cleaned_data["amount"],
                                    description=form.cleaned_data["description"],
                                    category=form.cleaned_data["productCategory"],
                                    image=form.cleaned_data["productImage"])
            newBid = Bid.objects.create(listing=newListing, bidder=request.user, amount=form.cleaned_data["amount"])
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
    if request.method == "POST":
        if 'bid' in request.POST:
            bidForm = NewBidForm(request.POST)
            if bidForm.is_valid():
                if bidForm.cleaned_data['bid'] <= listing.currentPrice:
                    return HttpResponseRedirect(reverse("error", kwargs={'listingID': listing.listingID}))
                else:
                    Bid.objects.filter(listing=Listing.objects.get(pk=listingID)).delete()
                    Bid.objects.create(amount=bidForm.cleaned_data['bid'], listing=Listing.objects.get(pk=listingID),
                                                bidder=request.user)
                    Listing.objects.filter(pk=listingID).update(currentPrice=bidForm.cleaned_data['bid'])
                    #listing.currentPrice = bidForm.cleaned_data['bid']
                    return HttpResponseRedirect(reverse("listing", kwargs={'username': listing.poster, 'listingID': listingID}))
            else:
                return HttpResponseRedirect(reverse("listing", kwargs={'username': listing.poster, 'listingID': listingID}))
        if 'comment' in request.POST:
            commentForm = NewCommentForm(request.POST)
            if commentForm.is_valid():
                comment = Comment.objects.create(listing=Listing.objects.get(pk=listingID),
                                            author=request.user, comment=commentForm.cleaned_data["comment"])
                return HttpResponseRedirect(reverse("listing", kwargs={'username': listing.poster, 'listingID': listingID}))
            else:
                return HttpResponseRedirect(reverse("listing", kwargs={'username': listing.poster, 'listingID': listingID}))
    else:
        user = User.objects.get(username=username)
        comments = Comment.objects.filter(listing=listingID)
        return render(request, "auctions/listing.html", {
            "listing": listing,
            'otherUser': user,
            'commentForm': NewCommentForm(),
            'bidForm': NewBidForm(),
            'comments': comments
        })

def makeBid(request, amount, listingID):
    listing = Listing.objects.get(pk=listingID)
    if listing.currentPrice >= amount:
        return HttpResponseRedirect(reverse("error", kwargs={'listingID': listing.listingID}))
    else:
        Bid.objects.filter(listing=Listing.objects.get(pk=listingID)).delete()
        Bid.objects.create(amount=amount, listing=Listing.objects.get(pk=listingID),
                                    bidder=request.user)
        Listing.objects.get(pk=listingID).update(currentPrice=amount)
        return HttpResponseRedirect(reverse("listing", kwargs={'username': listing.poster, 'listingID': listingID}))

def addWatchList(request, listingID):
    listing = Listing.objects.get(pk=listingID)
    user = request.user
    if listing not in request.user.watchList.all():
        user.watchList.add(listing)
    return HttpResponseRedirect(reverse("watchlist"))

def watchList(request):
    user = request.user
    return render(request, 'auctions/watchlist.html', {
        'watchlist': user.watchList.all()
    })