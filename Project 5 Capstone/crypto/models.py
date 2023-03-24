from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    buy_price = models.DecimalField(max_digits=10, decimal_places=2)
    buy_quantity = models.IntegerField()
    name = models.CharField(max_length=10)
    ticker = models.CharField(max_length=20)    