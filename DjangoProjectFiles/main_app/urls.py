from django.urls import path
from . import views

urlpatterns = [
    # defined a randon view for home so I could view the page
    path('', views.chat_hub, name='home'),
    path('chats/', views.chat_hub, name='chat_hub'),
    path('chats/<str:pk>', views.chat_page, name='chats'),
]