from django.contrib import admin
from .models import Listing, Bid, Comment, Watchlist, User, AbstractUser


# Register your models here.
class ListingAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
        "start_price",
        "current_price",
        "start_date",
        "end_date",
        "seller",
        "image",
    )


admin.site.register(Listing, ListingAdmin)
admin.site.register(Watchlist)
admin.site.register(User)
