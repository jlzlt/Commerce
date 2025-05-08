from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxLengthValidator



class User(AbstractUser):
    watchlist = models.ManyToManyField("Listing", blank=True, related_name="watched_by")


class Listing(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", blank=False)
    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(validators=[MaxLengthValidator(1000)], blank=False)
    start_bid = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    final_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.URLField(max_length=255, blank=True)
    category = models.ForeignKey("Categories", on_delete=models.SET_NULL, null=True, blank=True, related_name="listings")
    closed = models.BooleanField(default=False)
    winner = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="won_auctions")

    def __str__(self):
        return f"{self.id}. {self.title}"

    def latest_price(self):
        highest_bid = self.bids.aggregate(max_bid=models.Max('bid'))['max_bid']
        return highest_bid if highest_bid is not None else self.start_bid
    
    def total_bids(self):
        return self.bids.count()
    
    def is_latest_bid_by_user(self, user):
        # Get the latest bid and check if it's made by the current user
        latest_bid = self.bids.order_by('-placed_at').first()
        if latest_bid:
            return latest_bid.bidder == user
        return False


class Bids(models.Model):
    placed_at = models.DateTimeField(auto_now_add=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids", blank=False)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids", blank=False)
    bid = models.DecimalField(max_digits=10, decimal_places=2, blank=False)


class Comments(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", blank=False)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments", blank=False)
    comment = models.TextField(validators=[MaxLengthValidator(1000)], blank=False)


class Categories(models.Model):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name
