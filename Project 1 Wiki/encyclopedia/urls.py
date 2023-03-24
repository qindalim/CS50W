from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:name>", views.entry, name="entry"),
    path("wiki/page/edit/<str:name>", views.editpage, name="editpage"),
    path("wiki/page/wiki/<str:name>", views.entry, name="reentry"),
    path("wiki/page/search", views.search, name="search"),
    path("wiki/page/new", views.newpage, name="newpage"),
    path("wiki/page/random", views.randompage, name="randompage")
]
