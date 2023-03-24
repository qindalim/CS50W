from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import *

def paging(request, posts):
    paginator = Paginator(posts, 10)
    if request.GET.get("page") != None:
        try:
            posts = paginator.page(request.GET.get("page"))
        except:
            posts = paginator.page(1)
    else:
        posts = paginator.page(1)
    return posts

@login_required
def index(request):
    posts = Post.objects.all().order_by("-datetime")
    posts = paging(request, posts)
    return render(request, "network/index.html", {"posts": posts})

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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

@login_required
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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)

        # Create profile
        profile = Profile()
        profile.user = user
        profile.save()

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def profile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(user=user).order_by("-datetime")
    current_profile = Profile.objects.get(user=request.user)

    posts = paging(request, posts)

    for i in current_profile.follower.all():
        print(i)
    return render(request, "network/profile.html",  {
        "user": user,
        "profile": profile,
        "posts": posts,
        "current_profile": current_profile
    })

@login_required
@csrf_exempt
def edit_post(request):
    if request.method == "POST":
        post_id = request.POST.get("id")
        new_post = request.POST.get("post")
        post = Post.objects.get(id=post_id)
        if post.user == request.user:
            post.post = new_post.strip()
            post.save()
            return JsonResponse({}, status=201)
    return


@login_required
@csrf_exempt
def add_post(request):
    if request.method == "POST":
        post = request.POST.get("post")
        if len(post) != 0:
            obj = Post()
            obj.post = post
            obj.user = request.user
            obj.save()
            return JsonResponse({
                "status": 201,
                "post_id": obj.id,
                "username": request.user.username,
                "datetime": obj.datetime.strftime("%B %d, %Y, %I:%M %p"),
            }, status=201)
    return

@login_required
@csrf_exempt
def like(request):
    if request.method == "POST":
        post_id = request.POST.get("id")
        liked = request.POST.get("liked")
        post = Post.objects.get(id=post_id)
        if liked == "no":
            post.like.add(request.user)
            liked = "yes"
        else:
            post.like.remove(request.user)
            liked = "no"
        post.save()
        return JsonResponse({"likes": post.like.count(), "liked": liked, "status": 201})
    return

@login_required
@csrf_exempt
def follow(request):
    if request.method == "POST":
        user = request.POST.get("user")
        action = request.POST.get("action")
        user = User.objects.get(username=user)
        profile = Profile.objects.get(user=request.user)
        
        if action == "Follow":
            profile.following.add(user)
            profile.save()
            profile = Profile.objects.get(user=user)
            profile.follower.add(request.user)
            profile.save()
            return JsonResponse({"status": 201, "follower_count": profile.follower.count(), "action": "Unfollow"}, status=201)
        else:
            profile.following.remove(user)
            profile.save()
            profile = Profile.objects.get(user=user)
            profile.follower.remove(request.user)
            profile.save()
            return JsonResponse({"status": 201, "follower_count": profile.follower.count(), "action": "Follow"}, status=201)
    return

@login_required
def following(request):
    following = Profile.objects.get(user=request.user).following.all()
    posts = Post.objects.filter(user__in=following).order_by("-datetime")

    posts = paging(request, posts)

    return render(request, "network/following.html", {"posts": posts})