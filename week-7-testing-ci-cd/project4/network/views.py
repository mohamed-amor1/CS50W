from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from .models import User, Post
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_protect


@csrf_exempt
def index(request):
    if request.method == "POST":
        form_id = request.POST.get("form_id")
        if form_id == "compose-form":
            username = request.user.username
            text = request.POST.get("compose-body")

            # Get the User instance for the author
            author = User.objects.get(username=username)

            post = Post.objects.create(author=author, text=text)
            return redirect("index")

    # Get the target_username based on the user profile being viewed
    target_username = None
    if request.user.is_authenticated:
        target_username = request.user.username

    posts = Post.objects.order_by("-timestamp")  # Order posts by most recent first
    return render(
        request,
        "network/index.html",
        {"posts": posts, "target_username": target_username},
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


@csrf_exempt
def user_profile_json(request, username):
    try:
        user = User.objects.get(username=username)
        posts = Post.objects.filter(author=user).order_by("-timestamp")
        posts_data = []

        for post in posts:
            post_data = {
                "author": post.author.username,
                "text": post.text,
                "timestamp": post.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "likes": post.likes,
            }
            posts_data.append(post_data)

        followers = [follower.username for follower in user.followers.all()]

        following_users = [u.username for u in user.following.all()]

        user_profile_data = {
            "username": user.username,
            "email": user.email,
            "followers": user.followers.count(),
            "following": user.following.count(),
            "posts": posts_data,
            "target_username": username,
            "following_users": following_users,
        }

        is_authenticated = request.user.is_authenticated
        current_username = request.user.username

        user_profile_data["is_authenticated"] = is_authenticated
        user_profile_data["current_username"] = current_username

        if is_authenticated:
            user_profile_data["is_following"] = current_username in followers

        return JsonResponse(user_profile_data)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found"}, status=404)


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


@csrf_protect
@login_required
def follow_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        target_user = get_object_or_404(User, username=username)

        target_user.followers.add(request.user)
        request.user.following.add(target_user)

        return JsonResponse(
            {
                "success": True,
                "action": "follow",
                "message": "Follow action successful.",
            },
            status=200,
        )

    return JsonResponse({"success": False, "error": "Invalid request."}, status=400)


@csrf_protect
@login_required
def unfollow_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        target_user = get_object_or_404(User, username=username)

        target_user.followers.remove(request.user)
        request.user.following.remove(target_user)

        target_user.save()  # Save the changes
        request.user.save()  # Save the changes

        return JsonResponse(
            {
                "success": True,
                "action": "unfollow",
                "message": "Unfollow action successful.",
                "followers_count": target_user.followers.count(),
            },
            status=200,
        )

    return JsonResponse({"success": False, "error": "Invalid request."}, status=400)
