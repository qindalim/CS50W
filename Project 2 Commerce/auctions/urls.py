from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("makelisting", views.makelisting, name="makelisting"),
    path("listing/<str:item_id>", views.showlisting, name="listing"),
    path("watchlist/<str:user_id>", views.watchlist, name="watchlist"),
    path("categories", views.categories, name="categories"),
    path("addtowatchlist/<str:item_id>", views.addtowatchlist, name="addtowatchlist"),
    path("removefromwatchlist/<str:item_id>", views.removefromwatchlist, name="removefromwatchlist"),
    path("bid/<str:item_id>", views.bid, name="bid"),
    path("closebid/<str:item_id>", views.closebid, name="closebid")    
]