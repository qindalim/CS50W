from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(User)
admin.site.register(Categories)
admin.site.register(Listings)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(Watchlist)