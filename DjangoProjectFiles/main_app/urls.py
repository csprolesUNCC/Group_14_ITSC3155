from django.urls import path
from . import views

urlpatterns = [
    path('chats/', views.chat_hub, name='chat_hub'),
    path('chats/<str:pk>', views.chat_page, name='chats'),
]