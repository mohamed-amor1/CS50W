from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    image = models.URLField(blank=True, null=True)

    CATEGORY_CHOICES = (
        ("Fashion", "Fashion"),
        ("Toys", "Toys"),
        ("Electronics", "Electronics"),
        ("Home", "Home"),
        ("Books", "Books"),
        ("Sports", "Sports"),
        ("Collectibles", "Collectibles"),
        ("Art", "Art"),
        ("Jewelry", "Jewelry"),
        ("Antiques", "Antiques"),
        ("Vehicles", "Vehicles"),
        ("Instruments", "Musical Instruments"),
        ("Tools", "Tools"),
        ("Appliances", "Appliances"),
        ("Beauty", "Beauty Products"),
        ("Gaming", "Gaming Consoles & Video Games"),
        ("Coins", "Coins & Currency"),
        ("Tickets", "Event Tickets"),
        ("Other", "Other"),
    )
    category = models.CharField(
        max_length=100, choices=CATEGORY_CHOICES, null=True, blank=True
    )

    def __str__(self):
        return self.title


class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bid on '{self.listing.title}' by {self.bidder.username}"


class Comment(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="comments"
    )
    commenter = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on '{self.listing.title}' by {self.commenter.username}"
