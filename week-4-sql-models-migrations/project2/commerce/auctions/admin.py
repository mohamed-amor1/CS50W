from django.contrib import admin
from .models import Listing, Bid, Comment, Watchlist, User


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


class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "is_staff", "is_active", "date_joined")
    list_filter = ("is_staff", "is_active")
    search_fields = ("username", "email")


admin.site.register(Listing, ListingAdmin)
admin.site.register(Watchlist)
admin.site.register(User, UserAdmin)
admin.site.register(Comment)
admin.site.register(Bid)
