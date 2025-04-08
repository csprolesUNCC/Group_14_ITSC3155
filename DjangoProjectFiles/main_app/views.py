from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from models import User, Chats
from forms import ChatForm

# Create your views here.

@login_required
def chat_page(request, pk):

    form = ChatForm()

    sender = sender.username
    receiver = pk

    # try to find receiver
    # if it doesn't exists
    # redirect to chat hub page

    if User.objects.get(username=receiver) is None:
        return redirect('chat_hub')

    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.sender = sender
            chat.receiver = receiver
            chat.save()
        

    # get chats between users
    chats = Chats.objects.filter(sender=sender, receiver=receiver).values()
    chats = chats | Chats.objects.filter(sender=receiver, receiver=sender).values()
    
    # order chats by descending time_sent
    chats = chats.order_by('-time_sent').values()

    context = {
        'form': form,
        'sender': sender,
        'receiver': receiver,
        'chats': chats,
    }
    return render(request, 'base/chat_room.html', context)

@login_required
def chat_hub(request):

    return render(request, 'base/chat_hub.html')