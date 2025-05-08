from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.utils import timezone

from .models import User, Listing, Bids
from .forms import CreateListingForm, PlaceBidForm, CommentForm


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        "listings": listings
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def create(request):
    if request.method == "POST":
        form = CreateListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            start_bid = form.cleaned_data['start_bid']
            pic_url = form.cleaned_data['pic_url']
            category = form.cleaned_data['category']
            description = form.cleaned_data['description']

            Listing.objects.create(
                title=title,
                start_bid=start_bid,
                image=pic_url,
                category=category,
                description=description,
                user=request.user
            )

            return redirect('index')

    else:
        form = CreateListingForm()

    return render(request, "auctions/create.html", {
        'form': form
    })

def listing(request, id):
    listing = get_object_or_404(Listing, id=id)
    current_bid = listing.latest_price()
    is_latest_bid_by_user = listing.is_latest_bid_by_user(request.user) if request.user.is_authenticated else False
    is_users_listing = (listing.user == request.user)
    comments = listing.comments.order_by('-created_at')

    comment_form = CommentForm()

    if request.method == 'POST':
        if 'place_bid' in request.POST:
            if not request.user.is_authenticated:
                messages.error(request, "You must be logged in to place a bid.")
                return redirect('listing', id=listing.id)
            
            elif listing.user == request.user:
                messages.error(request, "Sellers cannot place bids on their own listings.")
                return redirect('listing', id=listing.id)

            form = PlaceBidForm(request.POST, current_bid=current_bid)
            if form.is_valid():
                bid_amount = form.cleaned_data['bid']

                Bids.objects.create(
                    listing=listing,
                    bidder=request.user,
                    bid=bid_amount
                )
                messages.success(request, f"Your bid of ${bid_amount} was placed successfully.")
                return redirect('listing', id=listing.id)
            
        elif 'add_comment' in request.POST:
            if not request.user.is_authenticated:
                messages.error(request, "You must be logged in to comment.")
                return redirect('listing', id=listing.id)
            
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.author = request.user
                comment.listing = listing
                comment.save()
                messages.success(request, "Comment added.")
                return redirect('listing', id=listing.id)
        
    form = PlaceBidForm(current_bid=current_bid)

    return render(request, "auctions/listing.html", {
        "listing": listing,
        "form": form,
        "comment_form": comment_form,
        "comments": comments,
        "is_latest_bid_by_user": is_latest_bid_by_user,
        "is_users_listing": is_users_listing,
    })

@login_required
def toggle_watchlist(request, id):
    listing = get_object_or_404(Listing, id=id)
    if listing in request.user.watchlist.all():
        request.user.watchlist.remove(listing)
        messages.success(request, f"'{listing.title}' removed from your watchlist.")
    else:
        request.user.watchlist.add(listing)
        messages.success(request, f"'{listing.title}' added to your watchlist.")
    return redirect('listing', id=listing.id)

@login_required
def close_auction(request, id):
    listing = get_object_or_404(Listing, id=id)

    if request.user != listing.user:
        messages.error(request, "Only the listing creator can close the auction.")
    
    if listing.closed:
        messages.warning(request, "This auction is already closed.")
    else:
        highest_bid = listing.bids.order_by('-bid', '-placed_at').first()
        if highest_bid:
            listing.winner = highest_bid.bidder
            listing.final_price = highest_bid.bid
        listing.closed = True
        listing.closed_at = timezone.now()
        listing.save()
        if listing.winner:
            messages.success(request, f"Auction closed successfully. User '{listing.winner}' won for ${listing.final_price}.")
        else:
            messages.success(request, "Auction closed successfully. This listing has ended with no bids. The item was not sold.")
    
    return redirect('listing', id=id)

@login_required
def watchlist(request):
    user_watchlist = request.user.watchlist.all()

    return render(request, 'auctions/watchlist.html', {
        'user_watchlist': user_watchlist,
    })