from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("about", views.about, name="about"),
    path("profile", views.profile, name="profile"),
    path("profit", views.profit, name="profit"),
    path("add", views.add_coin, name="add"),
    path("delete/<id>", views.delete_coin, name="delete"),
]