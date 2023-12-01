from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField('Listing', blank=True)
    pass

class Listing(models.Model):
    auction_open = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product_title = models.CharField(max_length=64)
    product_description = models.CharField(max_length=255)
    product_startingBid = models.IntegerField()
    product_currentBidder = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    product_category = models.CharField(max_length=64, blank=True)
    image_url = models.CharField(max_length=255, blank=True)

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid_amount = models.IntegerField()
    product = models.ForeignKey(Listing, on_delete=models.CASCADE)
    product_poster = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.CharField(max_length=255)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE)
    product_poster = models.ForeignKey(User, on_delete=models.CASCADE)