from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import User, Chat

# Create your views here.

@login_required
def chat_page(request, pk):

    sender = request.user.username
    receiver = pk

    # validates url pk that user exists
    if User.objects.get(username=receiver) is None:
        return redirect('chat_hub')

    if request.method == 'POST':
        c = Chat(
            sender=request.POST.get('sender'),
            receiver=request.POST.get('receiver'),
            body=request.POST.get('body')
        )
        c.save()
        
    # get chats between users
    chats = Chat.objects.filter(Q(sender=sender, receiver=receiver) | Q(sender=receiver, receiver=sender))

    # order chats by descending time_sent
    chats = chats.order_by('-time_sent')

    context = {
        'sender': sender,
        'receiver': receiver,
        'chats': chats,
    }
    return render(request, 'base/chat_room.html', context)

@login_required
def chat_hub(request):

    return render(request, 'base/chat_hub.html')