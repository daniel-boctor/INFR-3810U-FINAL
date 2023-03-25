from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator

# Create your models here.

class User(AbstractUser):
    address = models.CharField(max_length=32)
    postal_code = models.CharField(max_length=6)
    country = models.CharField(max_length=16)

class Listing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=32)
    price = models.DecimalField(decimal_places=2, max_digits=6, validators=[MinValueValidator(0.01)])
    image = models.URLField(null=True, blank=True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    review = models.CharField(max_length=32)
    recommend = models.BooleanField(default=False)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)