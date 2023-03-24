import json
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import *

# Create your views here.
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
            return render(request, "crypto/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "crypto/login.html")

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
            return render(request, "crypto/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "crypto/register.html", {
                "message": "Username already taken."
            })
        login(request, user)

        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "crypto/register.html")

@login_required
def index(request):
    return render(request, "crypto/index.html", {
        "coins": Portfolio.objects.all() 
    })

@login_required
def about(request):
    return render(request, "crypto/about.html")

@login_required
def profile(request):
    return render(request, "crypto/profile.html")

@login_required
def profit(request):
    return render(request, "crypto/profit.html", {
        "coins": Portfolio.objects.all() 
    })   

@csrf_exempt
@login_required
def add_coin(request):
    data = json.loads(request.body)

    coin = data.get("coin", "")
    ticker = data.get("ticker", "")
    buy_price = data.get("buy_price", "")
    buy_quantity = data.get("buy_quantity", "")

    portfolio = Portfolio(
        user = request.user,
        name = coin,
        ticker = ticker,
        buy_price = buy_price,
        buy_quantity = buy_quantity
    )

    portfolio.save()
    return render(request, "crypto/index.html", {
        "coins": Portfolio.objects.all() 
    })

@csrf_exempt
@login_required
def delete_coin(request, id):
    Portfolio.objects.filter(id=id).delete()
    return render(request, "crypto/index.html", {
        "coins": Portfolio.objects.all() 
    })
