from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Chat

# Create your views here.

@login_required(login_url='login')
def home(request):
    return render(request, 'base/home.html')

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
    return render(request, 'base/create_listing.html', {'form': form})
