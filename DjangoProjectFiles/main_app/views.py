from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .models import Chat

# Create your views here.

# Uncomment once login/register works
#@login_required
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