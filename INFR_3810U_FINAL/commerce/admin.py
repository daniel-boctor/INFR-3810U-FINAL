from django.contrib import admin
from .models import User, Listing, Order, Review, Wishlist

# Register your models here.

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Order)
admin.site.register(Review)
admin.site.register(Wishlist)