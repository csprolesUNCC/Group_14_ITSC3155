from django.shortcuts import render
from .models import Message

# Create your views here.

def chat_page(request, pk):

    # curr_user = request.user.

    return render(request, 'base/chat_room.html')