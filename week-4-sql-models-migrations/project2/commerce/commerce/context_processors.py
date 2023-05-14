from auctions.models import Watchlist


def watchlist_count(request):
    watchlist_count = 0  # Initialize with default value

    if request.user.is_authenticated:
        watchlist = Watchlist.objects.filter(user=request.user).first()
        if watchlist is not None:
            watchlist_count = watchlist.listings.count()

    return {"watchlist_count": watchlist_count}
