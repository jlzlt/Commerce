from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxLengthValidator



class User(AbstractUser):
    pass


class Listing(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings", blank=False)
    title = models.CharField(max_length=64, blank=False)
    description = models.TextField(validators=[MaxLengthValidator(1000)], blank=False)
    start_bid = models.DecimalField(max_digits=10, decimal_places=2, blank=False)
    image = models.URLField(max_length=255, blank=True)
    category = models.CharField(max_length=64, blank=True)

    def latest_price(self):
        highest_bid = self.bids.aggregate(max_bid=models.Max('bid'))['max_bid']
        return highest_bid if highest_bid is not None else self.start_bid


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