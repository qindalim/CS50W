from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *
from .forms import *

def index(request):
    return render(request, "auctions/index.html", 
    {"listings": Listings.objects.filter(is_closed=False)
    })

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
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
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
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def makelisting(request):
    if request.method == "POST":
        form = Createlistingform(request.POST)

        if form.is_valid():
            user = request.user
            name = form.cleaned_data["name"]
            description = form.cleaned_data["description"]
            price = form.cleaned_data["price"]
            image = form.cleaned_data["image"]
            category_id = Categories.objects.get(id=request.POST["categories"])
            Listings.objects.create(user=user, name=name, description=description, price=price, image=image, category=category_id)

        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/makelisting.html", {
            "createlistingform": Createlistingform(),
            "categories": Categories.objects.all()
        })

@login_required
def showlisting(request, item_id):
    listing = Listings.objects.get(id=item_id)
    user = request.user

    if listing.user == user: 
        is_seller = True 
    else: 
        is_seller = False

    category = Categories.objects.get(category=listing.category)

    if request.method == "POST":
        comment = request.POST["comment"]
        if comment != "":
            Comments.objects.create(user=user, listing=listing, comment=comment)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "category": category,
        "comments":Comments.objects.filter(listing=listing.id), 
        "is_watching": Watchlist.objects.filter(user=user, listing=listing).values("is_watching"), 
        "is_seller": is_seller
    })

@login_required
def watchlist(request, user_id):
    item_ids = Watchlist.objects.filter(user=request.user, is_watching=True).values("listing")
    listing = Listings.objects.filter(id__in=item_ids)

    return render(request, "auctions/watchlist.html", {
        "listings": listing
    })

def categories(request):
    listings = None
    category = None

    if request.method == "POST":
        category = request.POST["categories"]
        listings = Listings.objects.filter(category = category)

    return render(request, "auctions/categories.html", {
        "categories": Categories.objects.all(),
        "category": Categories.objects.get(id=category).category if category is not None else "",
        "listings": listings
    })


@login_required
def addtowatchlist(request, item_id):
    listing = Listings.objects.get(id=item_id)
    user = request.user

    if listing.user == user: 
        is_seller = True 
    else: 
        is_seller = False

    category = Categories.objects.get(category=listing.category)
    comments = Comments.objects.filter(listing=listing.id)
    watchlist = Watchlist.objects.filter(user=user, listing=listing)

    if watchlist:
        watchlist = Watchlist.objects.get(user=user, listing=listing)
        watchlist.is_watching = True
        watchlist.save()
    else:
        Watchlist.objects.create(user=user, listing=listing, is_watching=True)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "is_seller": is_seller,
        "category": category,
        "comments": comments, 
        "is_watching": Watchlist.objects.get(user=user, listing=listing).is_watching
    })

@login_required
def removefromwatchlist(request, item_id):
    listing = Listings.objects.get(id=item_id)
    user = request.user

    if listing.user == user: 
        is_seller = True 
    else: 
        is_seller = False

    category = Categories.objects.get(category=listing.category)
    comments = Comments.objects.filter(listing=listing.id)
    watchlist = Watchlist.objects.filter(user=user, listing=listing)

    if watchlist:
        watchlist = Watchlist.objects.get(user=user, listing=listing)

    watchlist.is_watching = False
    watchlist.save()

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "category": category,
        "comments": comments, 
        "is_watching": Watchlist.objects.get(user=user, listing=listing).is_watching, 
        "is_seller": is_seller
    })

@login_required
def bid(request, item_id):
    listing = Listings.objects.get(id=item_id)
    user = request.user

    if listing.user == user: 
        is_seller = True 
    else: 
        is_seller = False

    category = Categories.objects.get(category=listing.category)
    comments = Comments.objects.filter(listing=listing.id)
    watchlist = Watchlist.objects.filter(user=user, listing=listing)
    
    if watchlist:
        watchlist = Watchlist.objects.get(user=user, listing=listing)
    
    if request.method == "POST":
        bid = request.POST["bid"]
        listing.price = float(bid)
        listing.save()
        Bids.objects.create(user=user, price=bid, listing=listing)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "category": category,
        "comments": comments, 
        "is_watching": watchlist, 
        "is_seller": is_seller
    })

@login_required
def closebid(request, item_id):
    listing = Listings.objects.get(id=item_id)
    user = request.user

    if listing.user == user: 
        is_seller = True 
    else: 
        is_seller = False
        
    category = Categories.objects.get(category=listing.category)
    comments = Comments.objects.filter(listing=listing.id)
    watchlist = Watchlist.objects.filter(user=user, listing=listing)
    
    if watchlist:
        watchlist = Watchlist.objects.get(user=user, listing=listing)

    listing.is_closed = True
    listing.save()
    winner = Bids.objects.get(price=listing.price, listing=listing).user
    is_winningbid = user.id == winner.id

    return render(request, "auctions/closebid.html", {
        "listing": listing,
        "category": category,
        "comments": comments, 
        "is_watching": watchlist, 
        "is_seller": is_seller,
        "is_winningbid": is_winningbid
    })