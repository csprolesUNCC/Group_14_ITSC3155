from django.urls import path
from . import views

urlpatterns = [
    path('chats/<str:pk>', views.chat_page, name='chats'),
]