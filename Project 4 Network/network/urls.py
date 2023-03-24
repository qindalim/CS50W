
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("like", views.like, name="like"),
    path("follow", views.follow, name="follow"),
    path("post/edit", views.edit_post, name="edit_post"),
    path("post/add", views.add_post, name="add_post"),
    path("user/<username>", views.profile, name="profile"),
    path("following", views.following, name="following")
]
