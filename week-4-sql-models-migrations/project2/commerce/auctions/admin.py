# This imports the Django admin module.
from django.contrib import admin

# This imports the models from the auctions app.
from .models import Listing, Bid, Comment, Watchlist, User


# This creates a new class that inherits from the Django admin ModelAdmin class.
class ListingAdmin(admin.ModelAdmin):
    # This specifies the fields that will be displayed in the admin list view.
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


# This creates a new class that inherits from the Django admin ModelAdmin class.
class UserAdmin(admin.ModelAdmin):
    # This specifies the fields that will be displayed in the admin list view.
    list_display = ("username", "email", "is_staff", "is_active", "date_joined")

    # This specifies the fields that will be used to filter the admin list view.
    list_filter = ("is_staff", "is_active")

    # This specifies the fields that can be searched in the admin list view.
    search_fields = ("username", "email")


# This registers the Listing model with the Django admin site.
admin.site.register(Listing, ListingAdmin)

# This registers the Watchlist model with the Django admin site.
admin.site.register(Watchlist)

# This registers the User model with the Django admin site, using the UserAdmin class.
admin.site.register(User, UserAdmin)

# This registers the Comment model with the Django admin site.
admin.site.register(Comment)

# This registers the Bid model with the Django admin site.
admin.site.register(Bid)
