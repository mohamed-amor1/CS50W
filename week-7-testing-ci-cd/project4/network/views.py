from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
from .models import User, Post


def index(request):
    if request.method == "POST":
        if "new-post" in request.POST:
            post_content = request.POST["post-content"]
            new_post = Post(content=post_content, user=request.user)
            new_post.save()
            return HttpResponseRedirect(reverse("index"))

        # Retrieve the liked post IDs for the authenticated user
    liked_post_ids = []
    if request.user.is_authenticated:
        liked_post_ids = request.user.liked_posts.values_list("id", flat=True)

    posts = Post.objects.all().order_by("-timestamp")
    paginator = Paginator(posts, 10)  # Show 10 posts per page

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "network/index.html",
        {
            "page_obj": page_obj,
            "liked_post_ids": liked_post_ids,
        },
    )


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
                "network/login.html",
                {"message": "Invalid username and/or password."},
            )
    else:
        return render(request, "network/login.html")


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
                request, "network/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request, "network/register.html", {"message": "Username already taken."}
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    user = request.user

    if user in post.likes.all():
        post.likes.remove(user)
        liked = False
    else:
        post.likes.add(user)
        liked = True

    like_count = post.likes.count()

    return JsonResponse({"likes_count": like_count, "liked": liked})


def profile(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(user=user).order_by("-timestamp")

    liked_post_ids = []
    if request.user.is_authenticated:
        liked_post_ids = request.user.liked_posts.values_list("id", flat=True)

    # Check if the authenticated user is following the profile user
    is_following = False
    if request.user.is_authenticated:
        is_following = request.user.following.filter(username=username).exists()

    followers = user.followers.count()
    following = user.following.count()

    # Pass the follow status of the current user
    follow_status = "follow" if not is_following else "unfollow"

    paginator = Paginator(posts, 10)  # Assuming 10 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "network/profile.html",
        {
            "user": user,
            "page_obj": page_obj,
            "liked_post_ids": liked_post_ids,
            "followers": followers,
            "following": following,
            "is_following": is_following,
            "follow_status": follow_status,  # Pass the follow status
        },
    )


@login_required
@csrf_protect
def follow_user(request, user_id):
    # Get the user to follow
    user_to_follow = get_object_or_404(User, id=user_id)

    # Add the user to follow to the current user's following
    request.user.following.add(user_to_follow)

    # Update the follower count for the user being followed
    user_to_follow.followers.add(request.user)

    # Return the updated follower count
    followers_count = user_to_follow.followers.count()
    return JsonResponse({"followers_count": followers_count})


@login_required
@csrf_protect
def unfollow_user(request, user_id):
    # Get the user to unfollow
    user_to_unfollow = get_object_or_404(User, id=user_id)

    # Remove the user to unfollow from the current user's following
    request.user.following.remove(user_to_unfollow)

    # Update the follower count for the user being unfollowed
    user_to_unfollow.followers.remove(request.user)

    # Return the updated follower count
    followers_count = user_to_unfollow.followers.count()
    return JsonResponse({"followers_count": followers_count})


@login_required
@csrf_protect
def following(request):
    liked_post_ids = []
    if request.user.is_authenticated:
        liked_post_ids = request.user.liked_posts.values_list("id", flat=True)
    following_users = request.user.following.all()
    posts = Post.objects.filter(user__in=following_users).order_by("-timestamp")
    paginator = Paginator(posts, 10)  # Assuming 10 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "network/following.html",
        {
            "page_obj": page_obj,
            "liked_post_ids": liked_post_ids,
        },
    )
