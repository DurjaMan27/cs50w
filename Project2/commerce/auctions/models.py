from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchList = models.ManyToManyField("Listing", related_name="listings")
    pass

class Listing(models.Model):
    CATEGORIES = (
        ("General", "General"),
        ("Fashion", "Fashion"),
        ("Toys", "Toys"),
        ("Electronics", "Electronics"),
        ("Home", "Home"),
    )
    listingID = models.AutoField(primary_key=True)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField(max_length=255)
    category = models.CharField(max_length=15, choices=CATEGORIES)
    image = models.URLField(blank=True)
    currentPrice = models.PositiveIntegerField()
    auctionOpen = models.BooleanField(default=True)

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=255)

class Bid(models.Model):
    bidID = models.AutoField(primary_key=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()