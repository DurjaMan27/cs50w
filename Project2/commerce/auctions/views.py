from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from .models import User, Listing, Comment, Bid

category_list = ["all", "fashion", "toys", "electronics", "home", "collectibles", "antiques"]
class NewListingForm(forms.Form):

    CATEGORY_CHOICES = [
        ('all', 'All'),
        ('home', 'Home'),
        ('fashion', 'Fashion'),
        ('toys', 'Toys'),
        ('electronics', 'Electronics'),
        ('collectibles', 'Collectibles'),
        ('antiques', 'Antiques')
    ]

    title = forms.CharField(label="Product", widget=forms.TextInput(attrs={'placeholder': 'Product Title'}))
    description = forms.CharField(label="Description", widget=forms.Textarea(attrs={'placeholder':'Product Description'}))
    startingBid = forms.IntegerField(label="Starting Bid")
    productCategory = forms.ChoiceField(label="category", choices=CATEGORY_CHOICES, required=False)
    productImage = forms.URLField(label="image", required=False)

class NewCommentForm(forms.Form):
    comment = forms.CharField(label="Comment", max_length=500)

class NewBidForm(forms.Form):
    bid_amount = forms.IntegerField(label="Bid")


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
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

@login_required
def newlisting(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            newListing = Listing(auction_open=True, user=request.user, product_title=form.cleaned_data["title"],
                                    product_description=form.cleaned_data["description"],
                                    product_startingBid=form.cleaned_data["startingBid"],
                                    product_category=form.cleaned_data["productCategory"],
                                    image_url=form.cleaned_data["productImage"])
            return HttpResponseRedirect(reverse("listing", kwargs={'username': request.user.id, 'product': newListing.product_title}))
        else:
            return render(request, "auctions/create.html", {
                "form": form
            })

    return render(request, "auctions/create.html", {
        "form": NewListingForm()
    })

def listing(request, username, product):
    listing = Listing.objects.get(product_title=product)

    comments = Comment.objects.filter(product=listing)
    bids = Bid.objects.get(product=listing)
    if request.method == "POST":
        bidForm = NewBidForm(request.POST, username=username, product=product)
        commentForm = NewCommentForm(request.POST, username=username, product=product)
        if 'bidSubmit' in request.POST:
            if bidForm.is_valid():
                # Finding the bidAmount from the submitted form data
                newBidAmount = int(request.POST["bid_amount"])

                if newBidAmount <= listing.product_startingBid:
                    return HttpResponse("Your bid is too low. Please enter a bid amount that is greater than the current bid.")
                else:
                    user = request.User

                    Bid.objects.delete(user=user, product=listing, product_poster=username)

                    new_bid = Bid(user=user, product=listing, product_poster=username, bid_amount = newBidAmount)
                    listing.product_startingBid = newBidAmount
                    listing.product_description = user

                    bids = Bid.objects.get(product=product, product_poster=username)
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
                newComment = request.POST["comment"]
                user = request.User

                new_bid = Comment(user=user, product=listing, product_poster=username, comment = newComment)

                comments = Comment.objects.get(product=product, product_poster=username)
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

def all_listings(request, category):
    if category == "all":
        return HttpResponseRedirect(reverse("index"))
    elif category == "error":
        return HttpResponseRedirect(reverse("error"))
    else:
        listings = Listing.objects.filter(product_category=category)
        return render(request, "auctions/allListings.html", {
            "listings": listings,
            "category": category.capitalize()
        })

def categories(request):
    categoryUpper = []
    for item in category_list:
        categoryUpper.append(item.capitalize())
    categoryZip = zip(category_list, categoryUpper)
    return render(request, "auctions/categories.html", {
        "categoryZip": categoryZip
    })

@login_required
def watchlist(request, listing):
    User.watchlist.add(listing)
    return render(request, "auctions/watchlist.html", {
        "watchlist": User.watchlist
    })

def close_auction(request, listing):
    listing.auction_open = False
    return HttpResponseRedirect(reverse("index"))

def error(request):
    System.out.println("I actually got here")
    return render(request, "auctions/error.html")
