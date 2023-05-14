from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Listing, Bid, Comment, Watchlist
from .forms import CreateListingForm
from datetime import datetime, timedelta
from django.http import JsonResponse


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {"listings": listings})


def login_view(request):
    if request.method == "POST":
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create_listing(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            image_url = form.cleaned_data["image"]
            category = form.cleaned_data["category"]

            # Create a new listing object
            listing = Listing(
                title=title,
                description=description,
                start_price=starting_bid,
                current_price=starting_bid,  # Set current price initially to starting bid
                category=category,
                end_date=datetime.now()
                + timedelta(days=7),  # Set end date to 7 days from now
                seller=request.user,
                image=image_url,
            )

            listing.save()

            # Redirect to a success page or the newly created listing page
            return redirect("listing_page", id=listing.id)
    else:
        form = CreateListingForm()

    return render(request, "auctions/create_listing.html", {"form": form})


def listing_page(request, id):
    listing = Listing.objects.get(pk=id)
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(
            user=request.user, listings=listing
        ).first()
    else:
        watchlist = None
    return render(
        request,
        "auctions/listing_page.html",
        {
            "listing": listing,
            "watchlist": watchlist,
        },
    )


@login_required
def watchlist(request):
    if request.method == "POST":
        listing_id = request.POST.get("listing_id")
        try:
            listing = Listing.objects.get(id=listing_id)
        except Listing.DoesNotExist:
            return redirect("watchlist")

        watchlist, _ = Watchlist.objects.get_or_create(user=request.user)

        if "addForm" in request.POST:
            watchlist.listings.add(listing)
        elif "deleteForm" in request.POST:
            watchlist.listings.remove(listing)

    watchlist = Watchlist.objects.filter(user=request.user).prefetch_related("listings")
    message = (
        "You don't have any items in your watchlist." if not watchlist.exists() else ""
    )
    return render(
        request, "auctions/watchlist.html", {"watchlist": watchlist, "message": message}
    )


def user(request, seller_id):
    seller = get_object_or_404(User, id=seller_id)
    listings = Listing.objects.filter(seller=seller)
    return render(request, "auctions/user.html", {"seller": seller, "listings": listings})


def categories(request):
    categories = Listing.objects.values_list("category", flat=True).distinct()
    return render(request, "auctions/categories.html", {"categories": categories})