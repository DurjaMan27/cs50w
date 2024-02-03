from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchList = models.ManyToManyField("Listing", related_name="listings")
    pass

class Listing(models.Model):
    CATEGORIES = {
        "Fashion": "Fashion",
        "Toys": "Toys",
        "Electronics": "Electronics",
        "Home": "Home",
        "General": "General"
    }
    listingID = models.AutoField(primary_key=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    datePosted = models.DateTimeField()
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=255)
    startingBid = models.PositiveIntegerField()
    currentBid = models.ForeignKey("Bid", on_delete=models.CASCADE, blank=True, related_name="currentBid")
    category = models.CharField(max_length=64, choices=CATEGORIES, blank=True)
    image = models.URLField(blank=True)

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=255)

class Bid(models.Model):
    bidID = models.AutoField(primary_key=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()