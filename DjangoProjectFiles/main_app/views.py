from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.cache import never_cache
from django.conf import settings
from django.core.exceptions import ValidationError

import os
import io
from .models import Chat, Listing, ViewHistory, Profile
from .forms import ListingForm
from PIL import Image
from django.core.files.base import ContentFile

# Create your views here.

@never_cache
@login_required(login_url='login')
def home(request):
    query = request.GET.get('q', '')
    if query:
        items = Listing.objects.filter(
            Q(textbook_name__icontains=query) |
            Q(college__icontains=query) |
            Q(course__icontains=query) |
            Q(class_name__icontains=query)
        ).order_by('-created')
    else:
        items = Listing.objects.all().order_by('-created')

    viewed_listings = request.session.get('viewed_listings', [])
    viewed_listings = [int(id) for id in viewed_listings if Listing.objects.filter(id=id).exists()]
    recent_viewed_items = []
    for listing_id in viewed_listings[:8]:
        try:
            listing = Listing.objects.get(id=listing_id)
            recent_viewed_items.append(listing)
        except Listing.DoesNotExist:
            continue
    request.session['viewed_listings'] = viewed_listings
    request.session.modified = True

    print(f"Home View - Viewed Listings: {viewed_listings}")
    print(f"Home View - Recent Items: {[(item.id, item.textbook_name, item.seller.username) for item in recent_viewed_items]}")
    
    context = {
        'items': items,
        'recent_items': recent_viewed_items,
        'search_query': query,
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

    sender = request.user.username
    receiver = request.GET.get("usr")
    userSelected = False

    if User.objects.filter(username=receiver).exists() and sender != receiver:    
        userSelected = True
    
    if request.method == "POST":
        messageBody = request.POST.get("msg")

        if messageBody is not None and messageBody != '':
            C = Chat(
                sender=sender,
                receiver=receiver,
                body=messageBody
            )
            C.save()

    chats = Chat.objects.filter(Q(sender=sender) | Q(receiver=sender))

    chatterUsernames = {sender}

    for chat in chats:
        chatterUsernames.add(chat.sender)
        chatterUsernames.add(chat.receiver)

    chatterUsernames.remove(sender)

    currentChats = chats.filter(Q(sender=sender, receiver=receiver)|Q(sender=receiver, receiver=sender)).order_by('-time_sent')

    context = {
        "userSelected" : userSelected,
        "sender": sender,
        "receiver" : receiver,
        "chatterUsernames" : chatterUsernames,
        "chats" : currentChats,
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
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        profile = Profile.objects.create(user=request.user, university='', bio='')
    
    user_listings = Listing.objects.filter(seller=request.user)  # Changed 'user' to 'seller'
    avatar_dir = os.path.join(settings.MEDIA_ROOT, 'avatars')
    os.makedirs(avatar_dir, exist_ok=True)
    avatars = [f for f in os.listdir(avatar_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
    context = {
    'user': request.user,        
    'profile': profile,          
    'user_listings': user_listings,
    'avatars': avatars,
}
    return render(request, 'base/profile.html', context)

@login_required
def update_profile(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        
        # Handle profile picture
        if 'profile_picture' in request.FILES:
            file = request.FILES['profile_picture']
            if not file.content_type.startswith('image/'):
                return redirect('profile')
            try:
                img = Image.open(file)
                img = img.resize((150, 150), Image.LANCZOS)
                output = io.BytesIO()
                img.save(output, format='JPEG', quality=85)
                output.seek(0)
                profile.avatar.save(file.name, ContentFile(output.read()), save=True)
            except Exception:
                return redirect('profile')
        elif 'selected_avatar' in request.POST and request.POST['selected_avatar']:
            avatar_path = f"avatars/{request.POST['selected_avatar']}"
            profile.avatar = avatar_path
        
        # Handle university and bio
        profile.university = request.POST.get('university', '')
        profile.bio = request.POST.get('bio', '')
        profile.save()
        
        return redirect('profile')
    return redirect('profile')

@login_required
def delete_profile_picture(request):
    if request.method == 'POST':
        profile = Profile.objects.get(user=request.user)
        if profile.avatar:
            profile.avatar.delete(save=True)
        return redirect('profile')
    return redirect('profile')


@login_required
def product(request, item_id):
    item = get_object_or_404(Listing, id=item_id)
    
    # Track viewed listing in session
    viewed_listings = request.session.get('viewed_listings', [])
    item_id = int(item_id)
    
    # Remove item_id if already in list, then add to start
    if item_id in viewed_listings:
        viewed_listings.remove(item_id)
    viewed_listings.insert(0, item_id)
    viewed_listings = viewed_listings[:10]  # Limit to 10
    request.session['viewed_listings'] = viewed_listings
    request.session.modified = True
    
    print(f"Product View - Viewed Listing ID: {item_id}, Seller: {item.seller.username}")
    print(f"Product View - Updated Viewed Listings: {viewed_listings}")
    
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
def edit_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)

    if request.method == 'POST':
        listing.textbook_name = request.POST.get('textbook_name')
        listing.course = request.POST.get('course')
        listing.condition = request.POST.get('condition')
        
        # Handle image upload if a new image is provided
        if 'image' in request.FILES:
            listing.image = request.FILES['image']
        
        listing.save()
        return redirect('profile')  # Redirect to the profile or wherever appropriate

    return render(request, 'edit_listing.html', {'listing': listing})



