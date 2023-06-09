from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import MyUserCreationForm, UserUpdateForm, ListingForm, ReviewForm
from .models import Listing, Order, Review, Wishlist
from django.forms import modelformset_factory
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, "commerce/index.html", {"listings": Listing.objects.all()})

@login_required
def my_listings(request):
    ListingFormSet = modelformset_factory(Listing, form=ListingForm, extra=1, max_num=10, absolute_max=10, can_delete=True)
    if request.method ==  "GET":
        listingformset = ListingFormSet(queryset=Listing.objects.filter(user=request.user))
    else:
        listingformset = ListingFormSet(request.POST, queryset=Listing.objects.filter(user=request.user))
        if listingformset.is_valid():
            instances = listingformset.save(commit=False)
            for obj in listingformset.deleted_objects:
                obj.delete()
                messages.success(request, f"{obj.name} was successfully deleted.", extra_tags="Success!")
            for instance in instances:
                instance.user = request.user
                instance.save()
                messages.success(request, f"{instance.name} was successfully saved.", extra_tags="Success!")
            return HttpResponseRedirect(reverse("my_listings"))
    return render(request, "commerce/my_listings.html", {"formset": listingformset})
     
def listing(request, pk):
    return render(request, "commerce/listing.html", {
        "listing": Listing.objects.get(pk=pk),
        "order": Order.objects.filter(user=request.user, listing=pk).exists() if request.user.is_authenticated else None,
        "wishlist": Wishlist.objects.filter(user=request.user, listing=pk).exists() if request.user.is_authenticated else None,
        "reviews": Review.objects.filter(listing=pk),
        "review_form": (ReviewForm(instance=Review.objects.get(user=request.user, listing=pk)) if Review.objects.filter(user=request.user, listing=pk).exists() else ReviewForm()) if request.user.is_authenticated else None,
        })

@login_required
def order(request, pk=None):
    if not pk:
        return render(request, "commerce/orders.html", {"orders": Order.objects.filter(user=request.user)})
    if Listing.objects.get(pk=pk).user == request.user:
        messages.error(request, f"You cannot purchase your own listing!", extra_tags="Error")
    elif Order.objects.filter(user=request.user, listing=pk).exists():
        pass
    else:
        if not request.user.address or not request.user.postal_code or not request.user.country:
            messages.error(request, f"Incomplete address information. Head to the account settings for {request.user} and complete all addressing information.", extra_tags="Error")
        else:
            listing = Listing.objects.get(pk=pk)
            order = Order (
                user = request.user,
                listing = listing
            )
            order.save()
    return HttpResponseRedirect(reverse("listing", args=[pk]))

@login_required
def review(request, pk=None):
    if not pk:
        return render(request, "commerce/review.html", {"reviews": Review.objects.filter(user=request.user)})
    else:
        if Review.objects.filter(user=request.user, listing=pk).exists():
            form = ReviewForm(request.POST, instance=Review.objects.get(user=request.user, listing=pk))
        else:
            form = ReviewForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.listing = Listing.objects.get(pk=pk)
            instance.save()
        else:
            for error in form.non_field_errors():
                messages.error(request, f"{error}", extra_tags="Error")
            for field in form:
                for error in field.errors:
                    messages.error(request, f"{error}", extra_tags=f"{field.label}")
        return HttpResponseRedirect(reverse("listing", args=[pk]))

@login_required
def wishlist(request, pk=None):
    if not pk:
        return render(request, "commerce/wishlist.html", {"wishlist": Wishlist.objects.filter(user=request.user)})
    if Wishlist.objects.filter(user=request.user, listing=pk).exists():
        Wishlist.objects.filter(user=request.user, listing=pk).delete()
    else:
        listing = Listing.objects.get(pk=pk)
        wish = Wishlist (
            user = request.user,
            listing = listing
        )
        wish.save()
    return HttpResponseRedirect(reverse("listing", args=[pk]))

def register(request):
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}", extra_tags="Success!")
            return HttpResponseRedirect(reverse("index"))
    else:
        form = MyUserCreationForm()
    return render(request, "commerce/auth/register.html", {"form": form})

@login_required
def user(request, username):
    if request.user.username == username:
        if request.method == "POST":
            form = UserUpdateForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                messages.success(request, f"Info saved.", extra_tags="Success!")
                return HttpResponseRedirect(reverse("user", args=[request.user.username]))
        else:
            form = UserUpdateForm(instance=request.user)
        return render(request, "commerce/user.html", {"form": form})