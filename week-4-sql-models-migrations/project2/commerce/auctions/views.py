from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, Listing, Bid, Comment, Watchlist
from .forms import CreateListingForm, CommentForm, BidForm
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.utils import timezone
from django.contrib import messages


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
    listing = get_object_or_404(Listing, pk=id)
    error_message = ""
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(
            user=request.user, listings=listing
        ).first()
    else:
        watchlist = None

    comments = Comment.objects.filter(listing=listing).order_by("timestamp")
    bid_count = listing.bids.count()
    highest_bid = listing.bids.order_by("-amount").first()

    is_owner = False
    has_won = False

    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        bid_form = BidForm(request.POST)

        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.commenter = request.user
            comment.listing = listing
            comment.save()
            comment_form = CommentForm()

        if bid_form.is_valid():
            amount = bid_form.cleaned_data["amount"]
            if amount > listing.current_price and not listing.closed:
                listing.current_price = amount
                listing.save()
                highest_bid = Bid.objects.create(
                    listing=listing,
                    bidder=request.user,
                    amount=amount,
                    timestamp=timezone.now(),
                )
                return redirect("listing_page", id=id)
            else:
                bid_form.add_error(
                    "amount", "Bid must be greater than the current price."
                )

        if request.user.is_authenticated and request.user == listing.seller:
            if request.POST.get("close_auction"):
                if not listing.closed:
                    highest_bid = listing.bids.order_by("-amount").first()
                    if highest_bid:
                        listing.winner = highest_bid.bidder
                        listing.closed = True
                        listing.save()
                        messages.success(
                            request,
                            f"Auction closed. Winner: {listing.winner.username}",
                        )
                    else:
                        error_message = "Auction cannot be closed as there are no bids."
                        messages.error(request, error_message)

                    return redirect("listing_page", id=id)
            else:
                is_owner = True

    else:
        comment_form = CommentForm()
        bid_form = BidForm()

        if request.user.is_authenticated and request.user == listing.seller:
            is_owner = True
        elif (
            request.user.is_authenticated
            and listing.closed
            and listing.winner_id == request.user.pk
        ):
            has_won = True

    return render(
        request,
        "auctions/listing_page.html",
        {
            "listing": listing,
            "watchlist": watchlist,
            "comments": comments,
            "comment_form": comment_form,
            "bid_form": bid_form,
            "bid_count": bid_count,
            "highest_bid": highest_bid,
            "is_owner": is_owner,
            "has_won": has_won,
            "error_message": error_message,
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
    return render(
        request, "auctions/user.html", {"seller": seller, "listings": listings}
    )


def categories(request):
    categories = (
        Listing.objects.values_list("category", flat=True)
        .distinct()
        .order_by("category")
    )
    return render(request, "auctions/categories.html", {"categories": categories})


def category_page(request, category):
    listings = Listing.objects.filter(category=category)

    return render(
        request,
        "auctions/category_page.html",
        {"listings": listings, "category": category},
    )


@login_required
def comments(request, listing_id):
    listing = get_object_or_404(Listing, id=listing_id)
    comments = Comment.objects.filter(listing=listing).order_by("-timestamp")

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.commenter = request.user
            comment.listing = listing
            comment.save()
    else:
        form = CommentForm()

    return render(
        request,
        "auctions/listing_page.html",
        {
            "listing": listing,
            "comments": comments,
            "form": form,
        },
    )
