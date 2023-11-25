from django.contrib import admin
from .models import User, Listing, Bid, Comment

class ListingAdmin(admin.ModelAdmin):
    list_display = ("auction_open", "user", "product_title", "product_description", "product_startingBid", "product_currentBidder",
                    "product_category", "image_url")
class BidAdmin(admin.ModelAdmin):
    list_display = ("user", "bid_amount", "product_title", "product_poster")

class CommentAdmin(admin.ModelAdmin):
    list_display = ("user", "comment", "product_title", "product_description")

# Register your models here.
admin.site.register(User)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)