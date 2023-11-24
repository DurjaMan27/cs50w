from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="")
    product_title = models.CharField(max_length=64)
    product_description = models.CharField(max_length=255)
    product_startingBid = models.IntegerField()
    product_category = models.CharField(blank=True)
    image_url = models.CharField(max_length=255, blank=True)

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="")
    bid_amount = models.IntegerField()
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="")

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="")
    comment = models.CharField(max_length=255)
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="")