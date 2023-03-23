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
        return render(request, "commerce/my_listings.html", {"formset": listingformset})
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

@login_required        
def listing(request, pk):
    return render(request, "commerce/listing.html", {
        "listing": Listing.objects.get(pk=pk),
        "order": Order.objects.filter(user=request.user, listing=pk).exists(),
        "wishlist": Wishlist.objects.filter(user=request.user, listing=pk).exists(),
        "reviews": Review.objects.filter(listing=pk),
        "review_form": ReviewForm()
        })

@login_required
def order(request, pk=None):
    if not pk:
        return render(request, "commerce/orders.html", {"orders": Order.objects.filter(user=request.user)})
    if Order.objects.filter(user=request.user, listing=pk).exists():
        pass
    else:
        listing = Listing.objects.get(pk=pk)
        wish = Order (
            user = request.user,
            listing = listing
        )
        wish.save()
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