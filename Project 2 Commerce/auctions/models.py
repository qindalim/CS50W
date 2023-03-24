from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class Categories(models.Model): 
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"

class Listings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    name = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name="single_category")
    categories = models.ManyToManyField(Categories, blank=True, related_name="all_categories")
    image = models.URLField(default='google.com')
    is_closed = models.BooleanField(default=False)

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return f"{self.user}: {self.comment}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,)
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE)
    is_watching = models.BooleanField(default=False)