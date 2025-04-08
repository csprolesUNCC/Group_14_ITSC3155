from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import User, Message

# Create your views here.

@login_required
def chat_page(request, pk):

    sender = request.user
    receiver = User.objects.get(username=pk)
    messages = Message.objects.filter(sender=sender, receiver=receiver).values() | Message.objects.filter(sender=receiver, receiver=sender).values() 

    # todo: handle adding message to model

    context = {
        'sender': sender,
        'receiver': receiver,
        'messages': messages
    }
    return render(request, 'base/chat_room.html', context)

@login_required
def chat_hub(request):

    return render(request, 'base/chat_hub.html')