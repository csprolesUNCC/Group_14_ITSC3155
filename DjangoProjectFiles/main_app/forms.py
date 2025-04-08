from django.forms import ModelForm
from models import Chats

class ChatForm(ModelForm):
    class Meta:
        model = Chats
        exclude = ["time_sent", "sender", "receiver"]