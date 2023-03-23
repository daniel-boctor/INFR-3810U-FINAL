from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("listing/<int:pk>", views.listing, name="listing"),
    path("order", views.order, name="order"),
    path("order/<int:pk>", views.order, name="order"),
    path("review", views.review, name="review"),
    path("review/<int:pk>", views.review, name="review"),
    path("wishlist", views.wishlist, name="wishlist"),
    path("wishlist/<int:pk>", views.wishlist, name="wishlist"),
    #auth routes
    path("login", auth_views.LoginView.as_view(template_name="commerce/auth/login.html"), name="login"),
    path("logout", auth_views.LogoutView.as_view(template_name="commerce/auth/logout.html"), name="logout"),
    path("register", views.register, name="register"),
    #user routes
    path("user/<str:username>", views.user, name="user")
]