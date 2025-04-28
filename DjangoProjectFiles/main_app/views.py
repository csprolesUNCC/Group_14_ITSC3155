from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Chat, Listing
from .forms import ListingForm




# Create your views here.

@login_required(login_url='login')
def home(request):
    items = Listing.objects.all().order_by('-created')  # newest first
    context = {
        'items': items,
        'recent_items': []  # you can add recent view tracking later
    }
    return render(request, 'base/home.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Replace with your actual dashboard route name
        else:
            return render(request, 'base/login.html', {'error': 'Invalid credentials'})

    return render(request, 'base/login.html')


def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        if password != confirm_password:
            return render(request, 'base/signup.html', {'error': 'Passwords do not match'})

        if User.objects.filter(username=username).exists():
            return render(request, 'base/signup.html', {'error': 'Username already taken'})

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')  # Or change to your actual dashboard route

    return render(request, 'base/signup.html')
  
# Uncomment once login/register works
@login_required(login_url='login')
def chats(request):

    sendingUsername = request.user.username
        
    chatsSent = Chat.objects.filter(sender=sendingUsername)
    chatsReceived = Chat.objects.filter(receiver=sendingUsername)
    
    chatters = set()

    for chatSent in chatsSent:
        chatters.add(chatSent.receiver)

    for chatReceived in chatsReceived:
        chatters.add(chatReceived.sender)

    if request.method == 'POST':
        receivingUsername = request.POST.get('receivingUsername')
        
        if request.POST.get('action') == 'sending_chat':
            
            body = request.POST.get('body')

            if body != '':
                c = Chat(
                    sender=sendingUsername,
                    receiver=receivingUsername,
                    body=body
                )
                c.save()
            

        chats = chatsSent.filter(receiver=receivingUsername) | chatsReceived.filter(sender=receivingUsername)
        chats = chats.order_by('-time_sent')
    else:
        receivingUsername = None
        chats = None

    context = {
        'sendingUsername':sendingUsername,
        'chatters':chatters,
        'receivingUsername':receivingUsername,
        'chats':chats,
    }

    return render(request, 'base/chats.html', context)
  
@login_required(login_url='login')
def createListing(request):
    form = ListingForm()
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()
            return redirect('home')  # or a listing confirmation page
    return render(request, 'base/create_listings.html', {'form': form})



@login_required
def profile(request):
    user_listings = Listing.objects.filter(seller=request.user).order_by('-created')
    return render(request, 'base/profile.html', {'user_listings': user_listings})

def product(request, item_id):
    item = get_object_or_404(Listing, id=item_id)
    return render(request, 'base/product.html', {'item': item})



@login_required
def delete_listing(request, item_id):
    # Get the item or return a 404 if it doesn't exist
    item = get_object_or_404(Listing, id=item_id)

    # Check if the user is the seller of the listing
    if item.seller == request.user:
        item.delete()  # Delete the item
        return redirect('profile')  # Reload the profile page
    else:
        # If the user is not the seller, deny the deletion
        return redirect('profile')  # Optionally, you can redirect to an error page
    



@login_required
def edit_listing(request, item_id):
    # Get the item or return a 404 if it doesn't exist
    item = get_object_or_404(Listing, id=item_id)

    # Check if the user is the seller of the listing
    if item.seller != request.user:
        return redirect('profile')  # Redirect if the user is not the seller
    
    # Handle POST request to update the item
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()  # Save the updated item
            return redirect('profile')  # Redirect to profile page after editing
    else:
        form = ListingForm(instance=item)  # Pre-populate form with existing data

    return render(request, 'base/edit_listing.html', {'form': form, 'item': item})




